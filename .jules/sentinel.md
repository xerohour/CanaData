## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Cache Manager
**Vulnerability:** `CacheManager` was using `pickle` to serialize and deserialize data from disk cache, enabling arbitrary code execution if an attacker modified the `.cache` files. Weak hashing (`md5`) was also used for generating cache keys.
**Learning:** Local caching mechanisms can act as a vector for privilege escalation or code execution if they use insecure deserialization formats like `pickle` and are tampered with.
**Prevention:** Always use safe serialization formats like `json` over `pickle` for caching, and use strong hashing algorithms like `sha256` for key generation to prevent collisions.
