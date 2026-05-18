## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Fix Insecure Deserialization
**Vulnerability:** Insecure deserialization via pickle in cache manager
**Learning:** Using pickle for caching allows arbitrary code execution if the cache file is compromised. json is a safer serialization format.
**Prevention:** Use json (or other safe formats) for data serialization instead of pickle to prevent code execution payloads.
