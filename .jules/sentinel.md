## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Insecure Deserialization in Disk Cache
**Vulnerability:** The cache manager used `pickle` for serializing API responses to disk, which is vulnerable to remote code execution if a malicious actor can modify or plant a `.cache` file on disk.
**Learning:** Even local caches shouldn't use insecure deserialization methods when standard, safe formats like JSON can represent the same structure.
**Prevention:** Always use `json` instead of `pickle` for caching dictionary data, and securely unlink legacy `.cache` files instead of attempting to migrate them.
