import json
import time
from cache_manager import CacheManager

manager = CacheManager()
manager.set("test_url", {"key": "value"})
data = manager.get("test_url")
print("Cache data:", data)
