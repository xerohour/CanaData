## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-18 - Fix Insecure Deserialization in Cache
**Vulnerability:** Found `pickle.load` being used to read disk cache files, exposing the application to arbitrary code execution if the cache directory is compromised or spoofed.
**Learning:** Using `pickle` for caching API data is unnecessary and dangerous since the data format (JSON-like dictionaries) can be safely serialized using standard JSON.
**Prevention:** Always use `json` instead of `pickle` for safe serialization of data, restricting deserialization to primitive data structures.
