## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The use of `pickle` for caching API responses allowed arbitrary code execution via insecure deserialization.
**Learning:** Even internal caching systems are vulnerable if they load serialized data from disk, which can potentially be modified by malicious local actors or if cache files are synced insecurely.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching data.
