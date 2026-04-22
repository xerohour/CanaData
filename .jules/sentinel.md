## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-03-05 - Insecure Deserialization via pickle
**Vulnerability:** The cache manager was using the insecure `pickle` library to serialize and deserialize data from disk.
**Learning:** `pickle` is vulnerable to arbitrary code execution if an attacker can write or manipulate the cache files.
**Prevention:** Use safer serialization formats like `json` whenever persisting data, especially when dealing with data schemas that only consist of primitives/dicts/lists.
