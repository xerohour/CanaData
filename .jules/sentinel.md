## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-03-18 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle.load` to deserialize data from disk, which is vulnerable to arbitrary code execution if a cache file is tampered with.
**Learning:** The `pickle` module is insecure against malicious data. Deserialization of untrusted data must use secure formats like JSON, which only handles data structures and not executable code.
**Prevention:** Utilize `json.load` and `json.dump` for serializing and deserializing cache data instead of `pickle`.
