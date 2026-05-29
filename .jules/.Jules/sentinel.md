## 2025-02-14 - Fix insecure deserialization in cache_manager
**Vulnerability:** The CacheManager used python's insecure pickle module to deserialize cached files from disk.
**Learning:** The pickle module should never be used on files that can be tampered with by a malicious user, as unpickling arbitrary objects can lead to Remote Code Execution.
**Prevention:** Always use safe serialization formats like json when deserializing untrusted data.
