## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-03-05 - Insecure Deserialization via Pickle
**Vulnerability:** cache_manager.py uses `pickle` for caching, which is vulnerable to arbitrary code execution upon deserialization.
**Learning:** Storing and loading cache data using `pickle` can be exploited if the cache is tampered with by an attacker. Text-based formats like `json` should be used instead.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching data.
