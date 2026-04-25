## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-04-25 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for disk persistence of `.cache` files. Using `pickle` is prohibited because it allows arbitrary code execution during deserialization if cache files are tampered with.
**Learning:** Data stored in the cache must be JSON-serializable to avoid insecure deserialization vulnerabilities.
**Prevention:** Migrate file formats from binary `pickle` to text-based `json` for cache files, and always handle `UnicodeDecodeError` to prevent crashes when encountering legacy binary files opened with text encoding.
