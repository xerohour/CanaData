import pytest
import concurrent.futures
import time
import requests
import json
from unittest.mock import patch, MagicMock
from concurrent_processor import ConcurrentMenuProcessor
from CanaData import CanaData

def mock_request(*args, **kwargs):
    time.sleep(0.01) # Simulate network latency
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "listing": {"id": args[0].split("/")[-2] if "listings" in args[0] else "1", "slug": "test-slug", "wmid": "wm1", "_type": "dispensary"},
        "categories": [{"items": [{"id": 1, "name": "Test Item", "price": {"amount": 50}}]}]
    }
    return mock_response

def test_concurrent_processor_thread_safety():
    # Test that results and errors lists are thread safe (they should be since the executor returns futures)
    locations = [{"slug": f"loc-{i}", "type": "dispensary"} for i in range(100)]

    processor = ConcurrentMenuProcessor(max_workers=20, rate_limit=0.0)

    def process_func(loc):
        time.sleep(0.01) # Simulate work
        if int(loc["slug"].split("-")[1]) % 10 == 0:
            raise ValueError("Simulated error")
        return {"items": [1, 2, 3]}

    results = processor.process_locations(locations, process_func)

    assert len(results) == 90
    assert len(processor.errors) == 10

@patch("CanaData.CanaData.do_request")
def test_canadata_concurrent_get_menus(mock_do_request):
    # Mock do_request to return legacy API response so it processes properly
    mock_do_request.return_value = 'break' # force skip discovery items to go to legacy url

    with patch("requests.get", side_effect=mock_request):
        cana = CanaData(optimize_processing=False) # optimized flattener groups by location id so it deduplicates if mock id is the same. using custom flattener ensures we see the raw length.

        # Mocking environment variables
        import os
        os.environ['USE_CONCURRENT_PROCESSING'] = 'true'
        os.environ['MAX_WORKERS'] = '10'
        os.environ['RATE_LIMIT'] = '0.0'

        cana.locations = [{"slug": f"loc-{i}", "type": "dispensary", "id": f"loc-{i}"} for i in range(50)]

        # We bypass getLocations and directly call getMenus
        cana.getMenus()

        # Assertions to check thread safety on shared data structures
        assert len(cana.totalLocations) == 50
        assert cana.menuItemsFound == 50
        assert len(cana.finishedMenuItems) == 50

def test_cache_manager_concurrency():
    from cache_manager import CacheManager
    import threading

    # Disable disk cache to focus on memory cache concurrency
    manager = CacheManager(memory_cache_size=1000, enable_disk_cache=False)

    def worker(worker_id):
        for i in range(100):
            key = f"url-{i}"
            # Write
            manager.set(key, {"data": worker_id})
            # Read
            val = manager.get(key)
            assert val is not None

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # the stats dictionary might have memory_hits instead of hits
    assert manager.stats.get('memory_hits', 0) + manager.stats.get('memory_misses', 0) > 0
