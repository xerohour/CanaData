## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-23 - Insecure Deserialization via Pickle
**Vulnerability:** The application used `pickle` for caching data to disk, allowing potential arbitrary code execution if a malicious actor tampered with the cache files.
**Learning:** Legacy cache files written by `pickle` are binary and will likely throw a `UnicodeDecodeError` or `JSONDecodeError` when read as text. Transitioning to `json` requires catching these exceptions to safely return `None` (a cache miss) and prevent application crashes.
**Prevention:** Avoid using `pickle` for caching or serializing data unless absolutely necessary and fully trusted. Prefer secure formats like `json` and ensure graceful degradation when parsing fails.
