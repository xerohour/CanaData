import json
from cache_manager import CacheManager
cache = CacheManager(cache_dir="test_cache")
cache.set("http://example.com", {"key": "value"})
data = cache.get("http://example.com")
print(data)
