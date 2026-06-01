## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-06-01 - Insecure Deserialization in Cache Manager
**Vulnerability:** The cache manager was using `pickle` to deserialize data from disk cache (`*.cache`), which is vulnerable to arbitrary code execution if the cache files are maliciously tampered with.
**Learning:** Even internal caching systems need secure serialization since local disk files could be tampered with by other processes.
**Prevention:** Always use secure, text-based formats like `json` instead of `pickle` for serializing data, properly handling legacy cleanup.
