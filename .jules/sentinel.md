## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-05-24 - Fix Insecure Deserialization in CacheManager
**Vulnerability:** Found `pickle` being used for disk caching in `cache_manager.py`, which is vulnerable to arbitrary code execution via insecure deserialization.
**Learning:** `pickle` deserializes executable objects, making it unsafe for untrusted data or any data stored on disk that could be tampered with.
**Prevention:** Always use secure serialization formats like `json` for data interchange and storage, unless explicitly required and carefully validated. Catch `UnicodeDecodeError` and `json.JSONDecodeError` to handle legacy/corrupt cache files.
