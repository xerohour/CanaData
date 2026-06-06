## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-06-06 - Insecure Deserialization in CacheManager
**Vulnerability:** cache_manager.py used pickle.load() and pickle.dump() to load and store data from disk, which is vulnerable to remote code execution (RCE) if an attacker can manipulate the cache files.
**Learning:** Using pickle for caching, while easy to serialize complex python objects, creates an insecure deserialization point. JSON is much safer since it's limited to native primitives.
**Prevention:** Use json serialization instead of pickle to save cache files, and avoid executing arbitrary code paths when reading back data.
