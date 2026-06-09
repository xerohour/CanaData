## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-05-18 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for disk caching. `pickle` is inherently insecure as it allows arbitrary code execution during deserialization if an attacker can manipulate the cache files.
**Learning:** Even internal caching mechanisms must treat stored data as potentially untrusted if the storage medium (disk) can be manipulated. Never use `pickle` for data that might cross trust boundaries or be tampered with.
**Prevention:** Use safe serialization formats like `json` instead of `pickle`. When migrating, ensure legacy cache files are safely deleted without attempting to deserialize them.
