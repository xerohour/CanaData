## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-06-15 - Insecure Deserialization via Pickle
**Vulnerability:** The cache manager used `pickle.load()` on user-accessible disk cache files, enabling Arbitrary Code Execution (RCE).
**Learning:** Python's `pickle` module is fundamentally insecure and can execute arbitrary payloads during deserialization.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching, and securely invalidate legacy serialized files without migrating them.
