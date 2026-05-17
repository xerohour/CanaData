## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-25 - Insecure Deserialization in Cache Manager
**Vulnerability:** The `CacheManager` used the `pickle` module for disk caching, which allows arbitrary code execution if a loaded file is tampered with.
**Learning:** Caching mechanisms often use `pickle` for convenience (handling complex Python objects), but this introduces significant risk when the cache directory is accessible.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` when reading data from disk, even for internal application caching.
