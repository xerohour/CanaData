## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle.load` on cache files, which can lead to arbitrary code execution if an attacker can write or modify a `.cache` file.
**Learning:** Python's `pickle` module is not secure against erroneous or maliciously constructed data. Never unpickle data received from an untrusted or unauthenticated source.
**Prevention:** Use a safe serialization format like `json` for caching, and ensure graceful handling of legacy format (e.g. `UnicodeDecodeError`) when migrating away from binary formats.
