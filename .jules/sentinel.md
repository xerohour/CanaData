## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-04-16 - Insecure Deserialization in Cache Manager
**Vulnerability:** The cache manager was using `pickle` which allows arbitrary code execution if an attacker can write malicious `.cache` files into the cache directory.
**Learning:** Avoid `pickle` for caching external data as it has inherent deserialization vulnerabilities.
**Prevention:** Use standard, safe serialization formats like `json` instead of `pickle`.
