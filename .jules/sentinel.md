## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-05-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` to serialize and deserialize cached API responses, allowing arbitrary code execution if a cache file was tampered with.
**Learning:** Using `pickle` for data that resides on disk exposes the application to RCE, as disk cache files are implicitly trusted by `pickle.load`.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for persisting data to disk. Ensure legacy binary files are handled gracefully by catching `UnicodeDecodeError` and `json.JSONDecodeError`.
