## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-03-01 - Insecure Deserialization in CacheManager
**Vulnerability:** Cache manager used `pickle` for serializing cache data to disk, allowing potential Arbitrary Code Execution if a cache file was tampered with by an attacker.
**Learning:** `pickle` is inherently insecure for deserializing untrusted or potentially tampered data because it allows arbitrary code execution. Local cache files can be modified by an attacker with local access.
**Prevention:** Use secure serialization formats like `json` instead of `pickle` when the cache content does not require complex object serialization, preventing insecure deserialization attacks.
