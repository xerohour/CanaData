## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-06-02 - Insecure Deserialization via Pickle in Cache
**Vulnerability:** The CacheManager used Python's `pickle` module to serialize and deserialize data from disk cache, making the application vulnerable to arbitrary code execution if an attacker could write to the cache directory.
**Learning:** Using `pickle` for storing data is inherently insecure, even for local caching. Text-based formats like JSON should always be used.
**Prevention:** Use secure serialization formats like `json` with text modes (`'r'`, `'w'`) and explicit `encoding='utf-8'` instead of binary formats for cache serialization. Remove obsolete exceptions like `pickle.PickleError` and `EOFError` and handle `json.JSONDecodeError` and `TypeError` instead. Also, ensure backward-compatible cleanup routines account for legacy file extensions (`.cache`).
