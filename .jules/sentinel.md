## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-06-10 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager was using the `pickle` module for disk caching. Unpickling data from disk can lead to arbitrary code execution if an attacker modifies or provides a malicious `.cache` file.
**Learning:** `pickle` is inherently insecure for deserializing untrusted data or files that could potentially be tampered with on disk.
**Prevention:** Use secure serialization formats like `json` instead of `pickle`. When migrating away from `pickle`, ensure legacy `.cache` files are deleted securely without unpickling them to prevent execution of previously placed malicious payloads.
