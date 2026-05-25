## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-25 - Insecure Deserialization via Pickle
**Vulnerability:** The application used `pickle` for caching API responses to disk, which is vulnerable to insecure deserialization (arbitrary code execution) if a malicious `.cache` file is loaded.
**Learning:** Even internal cache managers can be an attack vector if an attacker gains access to the cache directory, as `pickle.load()` executes arbitrary code during deserialization.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching and data storage.
