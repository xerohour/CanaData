import pytest
import responses
from cache_manager import CacheManager
from cached_api_client import CachedAPIClient
from concurrent.futures import ThreadPoolExecutor

@responses.activate
def test_high_concurrency():
    for i in range(50):
        responses.add(responses.GET, f"http://test.com/{i}", json={"id": i}, status=200)

    cm = CacheManager()
    client = CachedAPIClient(cm)

    def fetch(url):
        return client.get(url, use_cache=False)

    urls = [f"http://test.com/{i}" for i in range(50)]
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch, urls))

    assert len(results) == 50
