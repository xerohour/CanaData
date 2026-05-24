## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-05-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The cache manager used pickle for disk caching, leading to potential arbitrary code execution if a user controls the cache files.
**Learning:** Built-in serialization libraries like pickle are unsafe for data that could potentially be tampered with by external actors.
**Prevention:** Use safe serialization formats like JSON for caching API responses and configuration data.
