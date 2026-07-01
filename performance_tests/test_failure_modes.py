import pytest
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cache_manager import CacheManager
from CanaData import CanaData

def test_cache_concurrent_access():
    cache = CacheManager(memory_cache_size=100)

    def worker(idx):
        cache.set(f"https://api.example.com/{idx}", {"data": f"value_{idx}"})
        cache.get(f"https://api.example.com/{idx}")

    threads = []
    for i in range(50):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(cache.memory_cache) == 50

def test_api_timeout_simulation(monkeypatch):
    import requests
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Connection timed out")

    monkeypatch.setattr(requests, "get", mock_get)
    scraper = CanaData(interactive_mode=False)
    scraper.cache_enabled = False  # force direct requests.get branch

    # do_request handles the exception and returns False
    result = scraper.do_request("https://fake.url/api")
    assert result is False
