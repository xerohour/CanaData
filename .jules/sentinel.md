## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Insecure Deserialization in Caching System
**Vulnerability:** The multi-tier caching system (`CacheManager`) used `pickle` to serialize and deserialize data to disk (`.cache` files), creating an insecure deserialization vulnerability that could lead to arbitrary code execution.
**Learning:** File-based caching mechanisms are susceptible to tampering if stored in accessible directories. Using unsafe deserialization functions like `pickle.load` on these files turns a file-write vulnerability into a remote code execution vulnerability.
**Prevention:** Always use safe serialization formats like `json` with strict type checking for disk-based caches, and validate the integrity of cached data before use.
