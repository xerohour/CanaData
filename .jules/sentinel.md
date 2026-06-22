## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-24 - Insecure Deserialization via Pickle
**Vulnerability:** The cache manager used `pickle.load()` to deserialize disk cache files, allowing potential arbitrary code execution if cache files were tampered with.
**Learning:** Python's built-in `pickle` module is fundamentally insecure against untrusted data. Even local cache files could be an attack vector in multi-user environments.
**Prevention:** Always use safe, text-based serialization formats like JSON for caching data unless cryptographically signing binary payloads.
