## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - Insecure Deserialization in Cache Manager
**Vulnerability:** The CacheManager used pickle for serialization/deserialization, allowing arbitrary code execution when reading malicious cache files.
**Learning:** File-based caching mechanisms are susceptible to manipulation. Replacing pickle with json is secure but requires careful exception handling (UnicodeDecodeError, JSONDecodeError) for legacy binary files.
**Prevention:** Always use secure formats like JSON for serialization instead of pickle, and ensure robust error handling for backward compatibility during migrations.
