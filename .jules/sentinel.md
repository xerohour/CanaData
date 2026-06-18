## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-25 - Insecure Deserialization in Cache Manager
**Vulnerability:** The cache manager used `pickle` for caching API responses, which is vulnerable to remote code execution via insecure deserialization if an attacker can write a malicious payload to a `.cache` file.
**Learning:** The use of `pickle` is inherently insecure for data from untrusted sources or if the storage medium could be tampered with. It can execute arbitrary code upon deserialization.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle`. When migrating, ensure legacy cache files (like `.cache`) are securely unlinked and ignored to prevent lingering payloads from executing.
