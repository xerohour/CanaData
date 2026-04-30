## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-04-30 - Insecure Deserialization in Caching
**Vulnerability:** The `CacheManager` used `pickle` for disk persistence, exposing the application to insecure deserialization vulnerabilities (RCE) if cache files were manipulated.
**Learning:** Python's `pickle` module is inherently unsafe for deserializing data from untrusted or accessible sources, including local file systems.
**Prevention:** Always use safe serialization formats like `json` for persisting data unless absolute trust in the data source is guaranteed.
