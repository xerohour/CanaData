## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-25 - Insecure Deserialization in Disk Cache
**Vulnerability:** The CacheManager was using the built-in `pickle` module to serialize and deserialize data from disk cache files, enabling arbitrary code execution if an attacker modifies or plants a `.cache` file.
**Learning:** Even local caches are susceptible to tampering; untrusted serialized data shouldn't be read using `pickle`. Legacy binary files might break when migrating from `pickle` to `json`.
**Prevention:** Use `json` for serialization/deserialization, and specifically catch `json.JSONDecodeError` and `UnicodeDecodeError` to safely discard unreadable legacy caches instead of crashing.
