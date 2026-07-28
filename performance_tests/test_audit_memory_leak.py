import os
import sys
import psutil
import gc
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from cache_manager import CacheManager

def test_memory_leak_caching():
    process = psutil.Process(os.getpid())
    gc.collect()
    start_memory = process.memory_info().rss

    cache = CacheManager(memory_cache_size=10000, enable_disk_cache=False)

    # Simulate a large number of cache entries to test memory footprint
    for i in range(5000):
        cache.set(f"http://test.com/{i}", {"data": "X" * 1024})  # 1KB per entry

    gc.collect()
    end_memory = process.memory_info().rss

    memory_diff_mb = (end_memory - start_memory) / (1024 * 1024)
    print(f"\n[METRIC] Memory Growth: {memory_diff_mb:.2f} MB")

    # We expect some growth, but let's assert it doesn't exceed a threshold
    assert memory_diff_mb < 50.0  # Should be less than 50MB
