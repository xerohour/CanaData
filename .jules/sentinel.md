## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-24 - Insecure Deserialization in Caching
**Vulnerability:** The cache system was using `pickle` to read and write persistent files to disk (`cache_manager.py`).
**Learning:** `pickle` is inherently unsafe and can execute arbitrary code upon deserialization. If an attacker can write to the cache directory, they can achieve arbitrary code execution.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` when persisting data.
