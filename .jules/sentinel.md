## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Cache Manager
**Vulnerability:** `CacheManager` used the `pickle` module to serialize and deserialize data from the disk cache. This allows arbitrary code execution if a user can write a malicious `.cache` file into the `cache_dir`.
**Learning:** File-based caching mechanisms that load serialized objects from disk are a prime target for insecure deserialization attacks if they use `pickle`. Even if the cache dir isn't directly exposed, it's safer to use data-only formats.
**Prevention:** Always use secure, data-only serialization formats like `json` instead of `pickle` when writing to and reading from disk or any untrusted source.
