## 2024-05-06 - Insecure Deserialization in CacheManager
**Vulnerability:** The application's CacheManager used `pickle` to serialize and deserialize data from disk caches.
**Learning:** Using `pickle` for caching allows arbitrary code execution if an attacker can manipulate or replace the underlying cache files.
**Prevention:** Always use safe serialization formats like JSON (`json.dump`/`json.load`) for disk caching systems instead of `pickle`.
