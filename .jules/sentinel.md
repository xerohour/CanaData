## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-03-02 - Insecure Deserialization in Disk Cache
**Vulnerability:** Python's `pickle` module was used in `cache_manager.py` to serialize and deserialize data to disk. Unpickling untrusted data can lead to arbitrary code execution.
**Learning:** Using `pickle` to store application state or cache on disk exposes the system to RCE if an attacker can manipulate or replace the cache files.
**Prevention:** Always use secure, text-based serialization formats like `json` when storing data on disk, especially when the cache files might be modified or are not perfectly isolated.
