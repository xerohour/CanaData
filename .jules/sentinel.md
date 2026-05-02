## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-05-02 - Insecure Deserialization in Cache Manager
**Vulnerability:** The `CacheManager` class used `pickle` to serialize and deserialize cached API responses from disk, which is vulnerable to arbitrary code execution if an attacker modifies the cache files.
**Learning:** Even caching mechanisms for non-sensitive data can introduce critical vulnerabilities like RCE if unsafe deserialization methods are used.
**Prevention:** Always use safe serialization formats like JSON for data caching, unless complex Python objects must be preserved, in which case cryptographically sign the cache files.
