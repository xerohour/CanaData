## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-25 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used the `pickle` module to store API responses and metadata to disk. This allowed insecure deserialization, where arbitrary code execution could occur if an attacker modified the `.cache` files.
**Learning:** `pickle` is inherently unsafe for storing any data that might be modified outside the strict control of the application, such as files in a local cache directory.
**Prevention:** Use safe serialization formats like `json` or `yaml` (with safe_load) for caching data, and avoid `pickle` entirely.
