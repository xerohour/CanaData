## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-02-18 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager was using Python's built-in `pickle` module to deserialize cache files from disk, allowing potential arbitrary code execution if an attacker could write to the cache directory.
**Learning:** Even internal cache systems must assume file storage could be tampered with. Using `pickle` is inherently unsafe for deserializing data that could be modified outside the application.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching or storing data, especially when handling data persistence on disk.
