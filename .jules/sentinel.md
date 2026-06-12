## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle.load()` on `.cache` files from disk, which allows arbitrary code execution if an attacker can manipulate the cache files on disk.
**Learning:** Using `pickle` to serialize and deserialize data even for seemingly safe internal caches creates a severe security vulnerability.
**Prevention:** Always use secure, text-based serialization formats like `json` with explicitly defined encoding (`utf-8`) instead of `pickle`, and ensure any legacy `.cache` files are safely unlinked instead of being read.
