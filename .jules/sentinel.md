## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-03-16 - Insecure Deserialization via Pickle
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing data to/from the `.cache` files on disk, which could allow arbitrary code execution if a cache file is modified or tampered with.
**Learning:** `pickle` is natively unsafe to use on potentially untrusted data since a malicious payload could trigger code execution upon deserialization. Cache files on disk are susceptible to modification.
**Prevention:** Use a safer serialization format like `json` instead of `pickle` for storing data to disk, unless there is a strong need to persist complex Python objects and the data source is absolutely trusted.
