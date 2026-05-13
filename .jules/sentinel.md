## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-05-13 - Insecure Deserialization in Disk Cache
**Vulnerability:** The multi-tier caching system `CacheManager` utilized Python's `pickle` module for writing cache files to disk, exposing the application to insecure deserialization attacks if a cache file was tampered with by a malicious user.
**Learning:** Avoid `pickle` for data serialization, especially when files are persisted to disk or can potentially be altered externally, as `pickle` executes arbitrary Python code during deserialization.
**Prevention:** Use secure serialization formats like `json` instead of `pickle`. When migrating, ensure file I/O operations are updated to text mode (`'r'`, `'w'`) with `encoding='utf-8'` and exception handling covers `json` related errors. Also, use file extensions like `.json` rather than `.cache` to accurately reflect the content and avoid misinterpretation.
