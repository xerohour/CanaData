## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Fix Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager was using `pickle` to serialize and deserialize data to/from disk. `pickle` is vulnerable to insecure deserialization, where an attacker can execute arbitrary code by injecting malicious pickled data.
**Learning:** `pickle` should never be used for data persistence or transmission where data integrity cannot be absolutely guaranteed. Even in local cache scenarios, an attacker with local file access could escalate privileges by modifying cache files.
**Prevention:** Use a secure serialization format like JSON (`json.dump` / `json.load`) for caching. When migrating from `pickle`, ensure legacy cache files (e.g. `.cache`) are removed alongside the new implementation.
