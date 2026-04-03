## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-04-03 - Fix Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing data to disk (`pickle.load`), creating a severe risk of Remote Code Execution (RCE) if an attacker could modify the cache files.
**Learning:** `pickle` was likely used for its convenience and ability to serialize complex Python objects, without realizing the security implications of reading untrusted disk files.
**Prevention:** Use safer serialization formats like `json` whenever persisting data to disk, especially in directories that might have permissive access or in web applications. Always treat data loaded from disk as untrusted if the disk could be tampered with.
