## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager used `pickle` for disk caching, which allows arbitrary code execution if a cache file is maliciously modified or injected.
**Learning:** Standard library modules like `pickle` are unsafe for handling data that could be tampered with, even in local cache directories.
**Prevention:** Always use safe serialization formats like JSON for caching data unless complex object graphs are strictly required and integrity is cryptographically guaranteed.
