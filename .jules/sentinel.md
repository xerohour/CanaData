## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-24 - Insecure Deserialization in Cache
**Vulnerability:** The disk cache used `pickle` which allowed arbitrary remote code execution via malicious `.cache` files.
**Learning:** Deserializing data from disk using `pickle` is inherently unsafe as it can execute arbitrary code during the unpickling process.
**Prevention:** Always use safe serialization formats like `json` for caching data to disk, and gracefully handle decode errors to migrate from legacy formats.
