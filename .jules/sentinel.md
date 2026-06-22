## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-05-15 - Insecure Deserialization in Cache Manager
**Vulnerability:** The `CacheManager` class used `pickle` to serialize and deserialize cached data from disk. `pickle` is inherently unsafe and can execute arbitrary code if the cache file is tampered with by a malicious actor.
**Learning:** Caching mechanisms are a common place to find insecure deserialization because developers treat the local filesystem as a trusted boundary, overlooking the risk of local file tampering.
**Prevention:** Always use safe, text-based serialization formats like `json` instead of `pickle` when storing or transmitting data, especially if it only contains basic data structures (like API JSON responses).
