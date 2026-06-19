## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-25 - Insecure Deserialization via Pickle
**Vulnerability:** The `CacheManager` used `pickle.load()` to deserialize disk cache files (`*.cache`), which could lead to arbitrary code execution if an attacker modifies or injects malicious cache files.
**Learning:** `pickle` is inherently insecure for deserializing untrusted or externally mutable data on disk.
**Prevention:** Always use safe serialization formats like `json` with `json.load()` and `json.dump()` when persisting data to disk, and securely unlink any legacy `.cache` files instead of attempting to migrate them.
