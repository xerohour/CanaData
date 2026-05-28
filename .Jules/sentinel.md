
## 2026-05-28 - Insecure Deserialization in Cache
**Vulnerability:** Use of `pickle` module to deserialize cache data from disk.
**Learning:** Python's `pickle` module can execute arbitrary code during deserialization, leading to critical RCE vulnerabilities if cache files are manipulated by an attacker.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching dictionary/string data unless dealing with complex Python objects (in which case, secure alternatives or strict signing should be used).
