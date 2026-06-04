## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-06-04 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager used `pickle.load` for disk cache, which is vulnerable to remote code execution (RCE) if an attacker can write or manipulate cache files.
**Learning:** `pickle` is fundamentally insecure for untrusted data. Disk cache files, even local ones, should not execute code during deserialization.
**Prevention:** Use secure serialization formats like `json` instead of `pickle` for caching data.
