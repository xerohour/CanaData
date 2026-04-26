## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-02-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for caching data to disk, leading to insecure deserialization vulnerability. Arbitrary code execution could occur if cache files were manipulated.
**Learning:** Never use `pickle` for caching or loading untrusted data.
**Prevention:** Use safer serialization formats like `json` to store and retrieve data. Ensure text encoding ('utf-8') is used. Handle exceptions like JSONDecodeError and UnicodeDecodeError safely.
