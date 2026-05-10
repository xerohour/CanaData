## 2024-05-10 - Insecure Deserialization in Disk Cache
**Vulnerability:** The application used `pickle` for serializing and deserializing disk cache entries in `cache_manager.py`. `pickle` is known to be unsafe and can lead to remote code execution if the cache files are tampered with.
**Learning:** Serializing data using `pickle` can expose the application to severe insecure deserialization vulnerabilities, as it allows arbitrary code execution upon deserialization.
**Prevention:** Use safer serialization formats like `json` for data that might be modified or when security is a concern, avoiding `pickle` entirely for untrusted or potentially tampered data.
