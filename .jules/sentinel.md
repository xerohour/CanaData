## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-03-08 - Insecure Deserialization via pickle
**Vulnerability:** The caching mechanism in `CacheManager` used `pickle` for storing and loading cached data. Unpickling data from untrusted sources or an improperly secured cache directory can lead to remote code execution (RCE).
**Learning:** Python's `pickle` module is fundamentally insecure for serializing data that might be modified by an attacker, as it allows arbitrary code execution during deserialization.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle`. When migrating, securely delete legacy cache files instead of attempting to read them to prevent execution of malicious payloads.
