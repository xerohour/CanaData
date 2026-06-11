## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-06-11 - Insecure Deserialization in CacheManager
**Vulnerability:** The disk cache implementation used `pickle` which is vulnerable to insecure deserialization (RCE) if an attacker can write malicious `.cache` files to the cache directory.
**Learning:** Even internal caching mechanisms should avoid `pickle` when the storage medium (disk) might be modifiable or untrusted.
**Prevention:** Use secure serialization formats like `json` instead of `pickle`. When migrating, ensure legacy `.cache` files are safely deleted without deserializing them.
