## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-05-21 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager used the `pickle` module to serialize and deserialize data from disk cache, which allows arbitrary code execution if an attacker modifies the cache files.
**Learning:** Using `pickle` for file-based caching inherently introduces a high severity risk (RCE) due to insecure deserialization.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` when persisting data, even if the data originates from trusted API responses, as local files can be tampered with.
