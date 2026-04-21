## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-18 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for storing and loading cache entries from disk.
**Learning:** Using `pickle` to deserialize files from the disk allows arbitrary code execution if an attacker can manipulate the cache files.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` when persisting data, even for internal caches, to prevent insecure deserialization vulnerabilities.
