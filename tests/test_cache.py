import pytest
import time
import os
import pickle
from pathlib import Path
from cache_manager import CacheManager

@pytest.fixture
def cache_manager(tmp_path):
    # Use a temporary directory for cache
    return CacheManager(
        cache_dir=str(tmp_path),
        memory_cache_size=3,
        memory_cache_ttl=1,
        disk_cache_ttl=2,
        enable_disk_cache=True
    )

def test_cache_set_get(cache_manager):
    url = "https://api.example.com/data"
    data = {"key": "value"}

    cache_manager.set(url, data)
    cached_data = cache_manager.get(url)

    assert cached_data == data
    assert cache_manager.stats['memory_hits'] == 1

def test_cache_miss(cache_manager):
    url = "https://api.example.com/missing"
    cached_data = cache_manager.get(url)

    assert cached_data is None
    assert cache_manager.stats['memory_misses'] == 1

def test_cache_eviction_lru(cache_manager):
    # Disable disk cache for this test to verify memory eviction strictly
    cache_manager.enable_disk_cache = False

    # Set 3 items (max size)
    cache_manager.set("url1", "data1")
    cache_manager.set("url2", "data2")
    cache_manager.set("url3", "data3")

    # Access url1 to make it most recently used
    cache_manager.get("url1")

    # Set 4th item, should evict url2 (LRU among remaining)
    # Order was: url1, url2, url3 -> set
    # Access url1 -> url2, url3, url1
    # Set url4 -> evict url2

    cache_manager.set("url4", "data4")

    assert cache_manager.get("url2") is None
    assert cache_manager.get("url1") == "data1"
    assert cache_manager.get("url3") == "data3"
    assert cache_manager.get("url4") == "data4"

def test_disk_cache_persistence(cache_manager, tmp_path):
    url = "https://api.example.com/persist"
    data = {"persistent": "data"}

    cache_manager.set(url, data)

    # Verify file exists
    cache_key = cache_manager._generate_cache_key(url)
    cache_file = Path(tmp_path) / f"{cache_key}.cache"
    assert cache_file.exists()

    # Clear memory cache
    cache_manager.memory_cache.clear()

    # Retrieve should hit disk
    cached_data = cache_manager.get(url)
    assert cached_data == data
    assert cache_manager.stats['disk_hits'] == 1

def test_cache_ttl(cache_manager):
    cache_manager.memory_cache_ttl = 0.1
    cache_manager.enable_disk_cache = False

    url = "https://api.example.com/ttl"
    cache_manager.set(url, "data")

    time.sleep(0.2)

    assert cache_manager.get(url) is None

def test_invalidate(cache_manager):
    cache_manager.set("https://api.example.com/1", "data1")
    cache_manager.set("https://api.example.com/2", "data2")
    cache_manager.set("https://other.com/1", "data3")

    cache_manager.invalidate("example.com")

    assert cache_manager.get("https://api.example.com/1") is None
    assert cache_manager.get("https://api.example.com/2") is None
    assert cache_manager.get("https://other.com/1") == "data3"
