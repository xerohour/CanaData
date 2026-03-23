## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-05-24 - Insecure Deserialization in CacheManager
**Vulnerability:** Arbitrary Code Execution (ACE) via `pickle.load` in the caching layer.
**Learning:** Using `pickle` for caching network responses creates a vector for code execution if the disk cache directory is writable by other local processes or if the cache is poisoned.
**Prevention:** Use standard serialization formats like `json` instead of executable serialization formats like `pickle`.
