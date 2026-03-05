## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager was using the `pickle` module to serialize and deserialize cached API responses to disk, which is vulnerable to Arbitrary Code Execution (ACE) if an attacker can tamper with the cache files.
**Learning:** `pickle` is inherently unsafe for any data that crosses trust boundaries, even local disk cache, as it allows arbitrary object instantiation and code execution upon deserialization.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching data. Ensure cache implementations are resilient against cache file tampering.
