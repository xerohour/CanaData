## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-03-02 - Insecure Deserialization in Cache Manager
**Vulnerability:** `cache_manager.py` used `pickle` for serializing and deserializing cache data to/from disk.
**Learning:** `pickle` is inherently insecure as it can execute arbitrary Python code during the unpickling process, leading to severe vulnerabilities if the cache files are tampered with.
**Prevention:** Use secure data serialization formats like `json` instead of `pickle` for caching objects, especially when persisting data to disk.
