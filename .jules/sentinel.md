## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing API responses to disk, which is vulnerable to insecure deserialization (arbitrary code execution) if cache files are manipulated by an attacker.
**Learning:** `pickle` should never be used for storing data on disk or transmitting it over a network due to its inherent security risks, even if the data originates from a trusted API, as the storage mechanism (disk) might be tampered with.
**Prevention:** Use secure serialization formats like `json` instead of `pickle`. When replacing legacy `pickle` systems, safely handle (e.g., delete without loading) any existing `.cache` files to prevent malicious execution during migration.
