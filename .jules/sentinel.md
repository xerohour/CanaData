## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## $(date +%Y-%m-%d) - Insecure Deserialization in Disk Cache
**Vulnerability:** The `CacheManager` used Python's `pickle` library to serialize and deserialize data to and from the disk cache. `pickle` is known to be vulnerable to insecure deserialization, where maliciously crafted data can execute arbitrary code upon deserialization.
**Learning:** Cache data was stored locally, but if the cache directory or files could be accessed or modified by an attacker, it could lead to Remote Code Execution (RCE).
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` when storing untrusted or potentially modifiable data on disk. When switching from `pickle` to `json`, ensure legacy cache files are handled gracefully by catching `UnicodeDecodeError` and `json.JSONDecodeError`.
