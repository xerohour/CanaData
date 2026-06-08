## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Cache Manager
**Vulnerability:** Used `pickle` for caching data. Pickle allows execution of arbitrary code upon deserialization, posing a critical risk if a cache file is tampered with by an attacker (or through path traversal / file replacement).
**Learning:** Never use `pickle` for storing data across sessions or environments where tampering might be possible. It's unsafe.
**Prevention:** Use a safe serialization format like `json` with text-based encoding. Ensure file operations correctly specify `encoding='utf-8'`.
