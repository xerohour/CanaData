## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-03-04 - [CRITICAL] Fix insecure deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing disk cache files, which is vulnerable to arbitrary code execution if an attacker can write or modify a `.cache` file in the cache directory.
**Learning:** Built-in Python serialization modules like `pickle` are unsafe for data that might be tampered with. Even cache files on disk represent a potential attack vector for local privilege escalation or RCE. When migrating from binary formats like `pickle` to text formats like `json`, we must handle `UnicodeDecodeError` to prevent crashes when the code encounters old binary cache files opened with a text encoding.
**Prevention:** Always use safe serialization formats like `json` for caching and data storage. Never use `pickle` unless the data source is fully trusted and cryptographically signed.
