## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2023-10-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` to serialize and deserialize data from the disk cache. `pickle` is inherently unsafe and can execute arbitrary code during deserialization if the cache file is tampered with.
**Learning:** Never use `pickle` to store data that might be read back later, especially in caching systems where files persist on disk and could be modified by a local attacker.
**Prevention:** Always use safe serialization formats like `json` for caching or data storage to prevent insecure deserialization vulnerabilities.
