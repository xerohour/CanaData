import os
import logging
import shutil

from cana_data import CanaData
from cache_manager import CacheManager
from optimized_data_processor import OptimizedDataProcessor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_concurrent_processing():
    """Test concurrent processing feature"""
    cana = CanaData(max_workers=5, rate_limit=0.5)
    cana.locations = [
        {"slug": "test-location-1", "type": "dispensary"},
        {"slug": "test-location-2", "type": "delivery"},
    ]

    assert cana.max_workers == 5
    assert cana.rate_limit == 0.5
    assert len(cana.locations) == 2


def test_caching():
    """Test caching feature"""
    cache_manager = CacheManager(
        cache_dir="test_cache",
        memory_cache_size=100,
        memory_cache_ttl=60,
        disk_cache_ttl=300,
        enable_disk_cache=True,
    )

    test_url = "https://api.example.com/test"
    test_data = {"test": "data", "value": 123}

    cache_manager.set(test_url, test_data)
    cached_data = cache_manager.get(test_url)

    assert cached_data == test_data

    cache_manager.invalidate()
    if os.path.isdir("test_cache"):
        shutil.rmtree("test_cache", ignore_errors=True)


def test_cache_eviction_respects_memory_cache_size():
    """Memory cache should evict oldest entries when over capacity."""
    cache_dir = "test_cache_eviction"
    cache_manager = CacheManager(
        cache_dir=cache_dir,
        memory_cache_size=2,
        memory_cache_ttl=60,
        disk_cache_ttl=300,
        enable_disk_cache=False,
    )

    cache_manager.set("https://api.example.com/a", {"id": "a"})
    cache_manager.set("https://api.example.com/b", {"id": "b"})
    cache_manager.set("https://api.example.com/c", {"id": "c"})

    assert len(cache_manager.memory_cache) == 2
    assert cache_manager.get("https://api.example.com/a") is None
    assert cache_manager.get("https://api.example.com/b") == {"id": "b"}
    assert cache_manager.get("https://api.example.com/c") == {"id": "c"}

    cache_manager.invalidate()
    if os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)


def test_cache_hit_rate_uses_lookup_counts():
    """Hit rate should be calculated from lookup attempts."""
    cache_dir = "test_cache_hit_rate"
    cache_manager = CacheManager(
        cache_dir=cache_dir,
        memory_cache_size=10,
        memory_cache_ttl=60,
        disk_cache_ttl=300,
        enable_disk_cache=False,
    )

    url_hit = "https://api.example.com/hit"
    url_miss = "https://api.example.com/miss"
    cache_manager.set(url_hit, {"ok": True})

    assert cache_manager.get(url_hit) == {"ok": True}
    assert cache_manager.get(url_miss) is None

    stats = cache_manager.get_stats()
    assert stats["memory_hits"] == 1
    assert stats["memory_misses"] == 1
    assert stats["hit_rate_percent"] == 50.0

    cache_manager.invalidate()
    if os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)


def test_data_processing():
    """Test optimized data processing"""
    processor = OptimizedDataProcessor(max_workers=2)

    sample_data = {
        "location1": [
            {
                "name": "Test Product 1",
                "price": {"amount": 50, "currency": "USD"},
                "category": "flower",
                "thc": "20%",
            },
            {
                "name": "Test Product 2",
                "price": {"amount": 75, "currency": "USD"},
                "category": "concentrate",
                "thc": "80%",
            },
        ]
    }

    processed_data = processor.process_menu_data(sample_data)
    assert len(processed_data) == 2


def test_integration():
    """Test integration of all features"""
    cana = CanaData(
        max_workers=5,
        rate_limit=0.5,
        cache_enabled=True,
        optimize_processing=True,
    )

    assert cana.cache_enabled is True
    assert cana.optimize_processing is True
