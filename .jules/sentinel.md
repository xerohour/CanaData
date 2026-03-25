## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-03-05 - Insecure Deserialization in Disk Cache
**Vulnerability:** The CacheManager used `pickle` for file-based caching, allowing arbitrary code execution if a cache file is modified.
**Learning:** Even local disk caches are vulnerable to insecure deserialization if an attacker gains filesystem access. Local persistence must use safe formats.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching or data persistence, unless cryptographically signed. Handle legacy formats gracefully during migration.
