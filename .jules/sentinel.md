## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-05-20 - Fix Insecure Deserialization in Cache Manager
**Vulnerability:** The cache manager (`cache_manager.py`) used the `pickle` module for serializing and deserializing data to/from disk.
**Learning:** Using `pickle` for caching is an insecure practice as it allows arbitrary code execution during deserialization if cache files are tampered with.
**Prevention:** Always use safe serialization formats like `json` instead of `pickle` for caching or data transfer, unless strict authentication and integrity checks are in place.
