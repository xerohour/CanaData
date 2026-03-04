## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-03-04 - Insecure Deserialization in CacheManager
**Vulnerability:** The `CacheManager` class used `pickle` to serialize and deserialize cached data. This is dangerous because `pickle.load()` can execute arbitrary code if the cached data is manipulated by an attacker with access to the file system.
**Learning:** `pickle` is not secure against erroneous or maliciously constructed data. It should never be used to deserialize data from untrusted or potentially compromised sources like disk caches.
**Prevention:** Use a secure serialization format like `json` instead of `pickle`. `json` is standard, lightweight, and does not allow execution of arbitrary code during deserialization.
