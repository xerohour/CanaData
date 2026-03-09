## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2023-10-27 - Insecure Deserialization in CacheManager
**Vulnerability:** The `CacheManager` used the `pickle` module to serialize and deserialize cached data from disk. Deserializing untrusted data with `pickle` can lead to arbitrary code execution.
**Learning:** Even internal cache files can pose a risk if an attacker gains write access to the filesystem. `pickle` should only be used in trusted environments where the serialized data source is completely controlled.
**Prevention:** Replace `pickle` with safe alternatives like `json` for serializing data, which only reconstructs basic data types and avoids arbitrary code execution risks.
