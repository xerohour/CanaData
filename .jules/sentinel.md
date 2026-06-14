## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-06-14 - Fix insecure deserialization in caching system
**Vulnerability:** The caching system used `pickle` for storing and retrieving API responses from the disk cache (`cache_manager.py`). This allows arbitrary code execution (RCE) if a malicious actor tampered with the `.cache` files on disk.
**Learning:** `pickle` is unsafe for deserializing data from untrusted or potentially modified sources, as it can instantiate arbitrary objects and execute code during deserialization.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching data. In this implementation, I also ensured backward compatibility by safely cleaning up legacy `.cache` files without attempting to deserialize them.
