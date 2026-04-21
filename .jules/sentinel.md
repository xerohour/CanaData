## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-03-08 - Cache Manager Insecure Deserialization
**Vulnerability:** The `CacheManager` used Python's `pickle` module (`pickle.dump` and `pickle.load`) to serialize and deserialize cached API responses to the disk cache.
**Learning:** This is an insecure deserialization vulnerability. If an attacker could write or modify files in the cache directory, they could craft a malicious pickle payload that executes arbitrary code when the application reads the cache file.
**Prevention:** Avoid using `pickle` for data serialization, especially when the stored files might be modified or come from untrusted sources. Use a safe format like `json` instead. When refactoring away from `pickle`, change the file extension (e.g., from `.cache` to `.json_cache`) to prevent old incompatible cache files from causing parsing errors.
