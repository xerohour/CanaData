## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Disk Cache
**Vulnerability:** The multi-tier caching system in `cache_manager.py` used the Python `pickle` module for persistent disk caching, which allows arbitrary code execution upon deserialization of tampered files.
**Learning:** Even local cache files can be attack vectors if they use insecure serialization formats. `pickle` is inherently unsafe for data that might be modified outside the application.
**Prevention:** Always use safe serialization formats like `json` for caching data to disk, unless cryptographic signing is used to guarantee file integrity.
