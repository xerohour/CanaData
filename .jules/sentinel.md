## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-19 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager used `pickle` for disk caching, which allows arbitrary code execution if a malicious payload is written to the cache directory.
**Learning:** Python's `pickle` module should never be used for caching or data serialization unless the data is strictly trusted, as it is inherently unsafe.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching and persisting data.
