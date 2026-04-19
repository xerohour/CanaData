## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-04-19 - Insecure Deserialization with Pickle
**Vulnerability:** The CacheManager was using `pickle` for caching, which is vulnerable to arbitrary code execution if the cache file is tampered with.
**Learning:** Always use secure formats like JSON for serialization when possible. `pickle` should only be used in trusted environments and never on untrusted or potentially modifiable files.
**Prevention:** Use `json` module for serialization and deserialization in caching mechanisms.
