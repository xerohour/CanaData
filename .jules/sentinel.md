## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-05-30 - Fix insecure deserialization in cache manager
**Vulnerability:** Use of `pickle` module for caching API responses allows arbitrary code execution via insecure deserialization.
**Learning:** Using `pickle` for caching is inherently unsafe if the cache file can be modified or spoofed.
**Prevention:** Use secure, data-only serialization formats like `json` with text-mode file I/O and UTF-8 encoding for all file-based caching.
