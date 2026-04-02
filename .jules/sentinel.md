## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-16 - Insecure Deserialization in Disk Cache
**Vulnerability:** The CacheManager used python's built-in `pickle` module for writing cache files to disk. Pickle is fundamentally insecure as it allows arbitrary code execution during deserialization if cache files are modified by an attacker.
**Learning:** File-based caching systems represent an often-overlooked attack vector. Even if the data originates internally, using an insecure deserialization method (like pickle) introduces risk if an attacker gains partial filesystem access or can control the cache directory.
**Prevention:** Always use secure, data-only serialization formats like `json` instead of executable serialization formats like `pickle` when persisting state or cache data. Include robust error handling (e.g., `json.JSONDecodeError` and `UnicodeDecodeError`) to gracefully fail if legacy or corrupted binary cache files are encountered.
