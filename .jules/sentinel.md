## 2024-05-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing cache data to/from disk.
**Learning:** `pickle` is vulnerable to insecure deserialization, which allows arbitrary code execution if a malicious actor tampered with the cache files.
**Prevention:** Use safer alternatives like `json` for serializing data when absolute trust cannot be established.
