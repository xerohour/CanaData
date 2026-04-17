## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-03-15 - Insecure Deserialization via Pickle in CacheManager
**Vulnerability:** The application used `pickle.load()` to deserialize cached data from disk, allowing potential arbitrary code execution if an attacker can manipulate or introduce malicious cache files.
**Learning:** `pickle` is inherently unsafe for deserialization of data from untrusted or accessible storage layers, as it can execute arbitrary Python objects upon loading.
**Prevention:** Use safe serialization formats like `json` to store structured data where arbitrary code execution is not needed. Ensure that data deserialization explicitly restricts object execution, utilizing `json.load()` instead of `pickle.load()` or `eval()`.
