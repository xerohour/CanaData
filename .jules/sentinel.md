## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Disk Cache
**Vulnerability:** The `CacheManager` used the `pickle` module to serialize and deserialize cached API responses to disk, which is vulnerable to arbitrary code execution if a cache file is tampered with.
**Learning:** `pickle` is inherently unsafe for deserializing data from a storage medium that could potentially be modified by an attacker.
**Prevention:** Use secure serialization formats like `json` instead of `pickle` when storing or transmitting data, especially if the data could originate from or be modified by an untrusted source. Handle legacy formats gracefully during migration.
