## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-12 - Insecure Deserialization in Cache Manager
**Vulnerability:** The `CacheManager` class was using Python's `pickle` module to serialize and deserialize cached data to disk (`*.cache` files).
**Learning:** `pickle` is inherently unsafe for deserialization because it can construct arbitrary Python objects, allowing an attacker to achieve Remote Code Execution (RCE) if they can modify the cache files on disk. Using a safer serialization format like `json` is necessary for mitigating this attack vector.
**Prevention:** Always use safe serialization formats (like `json`) instead of `pickle` for data that persists to disk and could potentially be tampered with. Only use `pickle` if you are completely certain that the data source is trustworthy and unmodifiable by a third party.
