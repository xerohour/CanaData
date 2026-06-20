## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-06-20 - Insecure Deserialization via Pickle
**Vulnerability:** The `CacheManager` class used the `pickle` module to serialize and deserialize cached data from disk. If a malicious user gained write access to the cache directory, they could craft a malicious pickle payload leading to arbitrary code execution when the cache is read.
**Learning:** Built-in serialization modules like `pickle` are unsafe for reading potentially untrusted or externally modifiable files.
**Prevention:** Always use safe serialization formats like `json` when reading/writing data to disk, unless cryptographic signing is used to verify the payload's integrity before deserialization.
