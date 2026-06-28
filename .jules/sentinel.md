## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-06-24 - Insecure Deserialization via Pickle
**Vulnerability:** The `CacheManager` class used Python's `pickle` module to serialize and deserialize data from the disk cache. If a cache file is maliciously modified, loading it can execute arbitrary code.
**Learning:** `pickle` is inherently insecure for data from untrusted sources, including local files that might be tampered with. Even internal caches should be protected from injection.
**Prevention:** Always use safe serialization formats like JSON (`json.dump`/`json.load`) for caching and data storage, unless strong cryptographic signing is used to verify the integrity of the pickle data before loading.
