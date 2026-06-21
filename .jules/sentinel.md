## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-06-21 - Fix insecure deserialization in CacheManager
**Vulnerability:** Insecure deserialization via `pickle` in `cache_manager.py`.
**Learning:** Using `pickle` for caching poses an RCE (Remote Code Execution) risk if cache files are tampered with. Legacy cache formats also require catching `UnicodeDecodeError` when migrating to `json` to gracefully handle old binary cache files.
**Prevention:** Use secure serialization formats like `json` instead of `pickle` for storing data.
