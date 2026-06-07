## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-03-01 - Insecure Deserialization in Caching
**Vulnerability:** Pickle used for file-based caching which can lead to remote code execution (RCE) if an attacker can write a file or manipulate a saved cache entry.
**Learning:** `pickle` deserialization is fundamentally insecure for untrusted data and could be targeted by a threat actor by hijacking cache artifacts. Legacy `.cache` files must also be handled securely as misses, rather than read.
**Prevention:** Never use `pickle` for persistent storage or messaging. Always use safe serialization formats like `json`.
