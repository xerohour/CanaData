## 2025-02-28 - Replace insecure pickle module in CacheManager
**Vulnerability:** Insecure deserialization via the `pickle` module in `cache_manager.py`.
**Learning:** Using `pickle` to serialize and deserialize data to/from disk is insecure. A malicious actor with access to the cache files could modify them to achieve Remote Code Execution (RCE).
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching and persisting application state, particularly when the storage location could be subject to unauthorized modification.
