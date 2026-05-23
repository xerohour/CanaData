## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Disk Cache
**Vulnerability:** The cache manager used Python's `pickle` module to serialize and deserialize data to disk (`_get_from_disk` and `_set_to_disk`). Loading arbitrary or manipulated `.cache` files via `pickle.load()` allows arbitrary code execution.
**Learning:** Even local disk caches can be vectors for critical vulnerabilities if insecure serialization formats are used, as local files can be tampered with or replaced.
**Prevention:** Always use secure, data-only serialization formats like `json` instead of `pickle` for caching or data exchange, unless strict integrity checks (like HMAC) are implemented.
