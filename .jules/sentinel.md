## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing data to/from the disk cache, allowing arbitrary code execution if cache files are manipulated by an attacker.
**Learning:** Standard library modules like `pickle` are unsafe for use with untrusted data or files that could be tampered with.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for storing data.
