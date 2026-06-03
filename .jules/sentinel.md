## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-03-05 - Insecure Deserialization via Pickle
**Vulnerability:** Used `pickle` in `cache_manager.py` for serializing and deserializing cached data. This is vulnerable to arbitrary code execution if a user modifies the cache payload (insecure deserialization).
**Learning:** Always prefer text-based structured data formats like JSON for serialization when complex objects aren't required, especially when file contents could be intercepted or manipulated.
**Prevention:** Use `json.dump` and `json.load` rather than `pickle`. Remember to manage file encodings correctly during file I/O operations.
