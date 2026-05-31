## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-31 - Insecure Deserialization in Cache Manager
**Vulnerability:** The cache system used `pickle` to serialize and deserialize data to/from disk.
**Learning:** Using `pickle` on files stored on disk poses a critical arbitrary code execution risk if an attacker can modify those cache files. `pickle` is not secure against erroneous or maliciously constructed data.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` when persisting data to disk, even for internal caching.
