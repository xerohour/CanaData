## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing cache data to and from disk. This can lead to arbitrary code execution if a malicious actor tampered with the cache files.
**Learning:** Using `pickle` for data persistence is unsafe unless the environment and data source are completely trusted. `json` is a safe alternative for standard data structures.
**Prevention:** Use `json` instead of `pickle` for caching dictionary/list-based API responses to prevent insecure deserialization risks.
