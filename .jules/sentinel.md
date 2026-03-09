## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-03-09 - Secure Pickle Deserialization with HMAC
**Vulnerability:** Found an insecure deserialization vulnerability due to CacheManager using unauthenticated `pickle` for its disk cache.
**Learning:** Insecure deserialization with `pickle` can lead to arbitrary code execution if the cache entries are tampered with. Replacing `pickle` entirely with `json` can cause functional regressions if the application caches complex objects (like custom classes, `datetime`, or tuples), since `json` does not support arbitrary Python objects.
**Prevention:** When `pickle` is required to cache arbitrary Python objects to an untrusted or unauthenticated disk space, the pickled payload must be cryptographically authenticated (e.g., using an HMAC signature with a secret key) before `pickle.loads()` is called. This verifies data integrity and authenticity, preventing malicious payload execution.
