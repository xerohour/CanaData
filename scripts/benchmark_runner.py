import time
from cache_manager import CacheManager
from cached_api_client import CachedAPIClient

def run_benchmark():
    cm = CacheManager()
    client = CachedAPIClient(cm)
    start = time.time()
    for i in range(100):
        try:
            _ = client.get(f"http://example.com/{i}", use_cache=False)
        except Exception:
            pass
    duration = time.time() - start
    print(f"Benchmark duration: {duration}s")

if __name__ == "__main__":
    run_benchmark()
