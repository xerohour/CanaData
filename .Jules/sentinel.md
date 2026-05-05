## 2024-05-05 - Fix Insecure Deserialization in CacheManager
**Vulnerability:** The `CacheManager` class used the `pickle` module to serialize and deserialize cached data from disk (`.cache` files).
**Learning:** `pickle` is vulnerable to arbitrary code execution if an attacker modifies the cache files.
**Prevention:** Use safer serialization formats like `json` instead of `pickle` when reading from or writing to the file system.
