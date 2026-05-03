## 2024-05-24 - Replace Insecure Pickle Deserialization
**Vulnerability:** Found insecure deserialization using `pickle` for caching API responses in `cache_manager.py`.
**Learning:** The cache module used `pickle` instead of `json`, which can lead to arbitrary code execution if a cache file is tampered with. Legacy cache files might cause `UnicodeDecodeError` when migrating to text mode.
**Prevention:** Use safer serialization formats like `json` instead of `pickle` for caching generic data structures, and handle legacy cache format transitions securely.
