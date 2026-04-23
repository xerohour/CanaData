import pytest
import concurrent.futures
import time
import requests
import json
import os
import responses
from unittest.mock import patch
from concurrent_processor import ConcurrentMenuProcessor
from CanaData import CanaData


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

@responses.activate
def test_canadata_concurrent_get_menus(monkeypatch):
    # Mocking environment variables BEFORE instantiation
    monkeypatch.setenv('USE_CONCURRENT_PROCESSING', 'true')
    monkeypatch.setenv('MAX_WORKERS', '10')
    monkeypatch.setenv('RATE_LIMIT', '0.0')

    cana = CanaData(optimize_processing=False, cache_enabled=False) # optimized flattener groups by location id so it deduplicates if mock id is the same. using custom flattener ensures we see the raw length. Disable cache to hit endpoints.

    # We mock 50 locations
    cana.locations = [{"slug": f"loc-{i}", "type": "dispensary", "id": f"loc-{i}"} for i in range(50)]

    for i in range(50):
        slug = f"loc-{i}"

        # We mock the discovery menu items endpoint.
        # process_menu_items_json requires standard structure: 'data': {'menu_items': [...]}
        discovery_url = f"{cana.baseUrl}/dispensaries/{slug}/menu_items?page=1&page_size=100&size=100"
        mock_response = {
            "data": {
                "menu_items": [
                    {
                        "id": 1,
                        "name": f"Test Item {i}",
                        "price": {"amount": 50}
                    }
                ]
            },
            "meta": {
                "total_menu_items": 1
            }
        }

        responses.add(responses.GET, discovery_url, json=mock_response, status=200)

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
