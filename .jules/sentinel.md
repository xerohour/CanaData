## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Insecure Deserialization in Disk Cache
**Vulnerability:** The CacheManager class used 'pickle' for persistent caching on disk, which allows arbitrary code execution if a cache file is maliciously crafted or tampered with.
**Learning:** Even internal caching mechanisms must assume disk files could be modified by unauthorized actors, leading to severe security risks when using unsafe deserialization formats like pickle.
**Prevention:** Always use secure, language-agnostic data serialization formats like JSON for disk storage unless executing arbitrary objects is explicitly required (and properly sandboxed).
