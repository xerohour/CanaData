## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-03-10 - Insecure Deserialization in Cache Manager
**Vulnerability:** The `CacheManager` used the `pickle` module for serializing and deserializing data to disk. This is vulnerable to insecure deserialization attacks if malicious data is placed in the cache.
**Learning:** Avoid using `pickle` for storing data across sessions, particularly when data origins might be untrusted or paths predictable.
**Prevention:** Use a secure serialization format like `json` to store arbitrary data instead of `pickle`. When handling legacy caches, gracefully catch decoding errors (e.g., `UnicodeDecodeError`, `json.JSONDecodeError`) to treat them as cache misses and replace them securely.
