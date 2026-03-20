## 2025-02-27 - Insecure Deserialization via Pickle in CacheManager
**Vulnerability:** The caching system `CacheManager` used Python's `pickle` module for persistent caching of API responses and internal data structures, exposing the application to arbitrary code execution if a maliciously crafted or modified cache file was read.
**Learning:** `pickle` deserializes Python objects, inherently running any code constructed within them. It must never be used with data that may be modified outside the context of the application memory. This system writes to disk cache directory (`cache/`), presenting a potential attack vector for unauthorized local users to embed arbitrary code in the process when it gets read later.
**Prevention:** Always use safe serialization formats, such as `json`, for data persistence. `json` safely limits structures to data without side effects upon loading.

## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
