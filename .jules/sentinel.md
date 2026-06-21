## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-03-09 - Insecure Deserialization in Caching
**Vulnerability:** Use of `pickle.load()` for loading files from disk caching allowed potential Arbitrary Code Execution (RCE).
**Learning:** System components utilizing local disk caching are vulnerable to RCE if insecure formats like `pickle` are used, as malicious actors might manipulate cache files.
**Prevention:** Use secure, data-only formats such as `json` for serialization and deserialization across trust boundaries, including local disk cache files.
