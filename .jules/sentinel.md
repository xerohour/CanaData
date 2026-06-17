## 2024-06-17 - Fix Path Traversal in CSV Export
**Vulnerability:** The `csv_maker` method in `CanaData` was vulnerable to path traversal because it concatenated unvalidated user input (the filename) with the destination directory, allowing output files to be written to arbitrary locations.
**Learning:** Even internal file-writing utility functions must strictly validate and sanitize input when the filename originates from or incorporates user-provided or dynamically scraped data, preventing local file pollution or overrides.
**Prevention:** Always implement a dedicated sanitization function (e.g., removing `../`, slashes, and invalid characters) for dynamically generated filenames, and ensure the resulting path remains securely within the intended output directory constraints.

## 2024-06-17 - Fix Insecure Deserialization in CacheManager
**Vulnerability:** The CacheManager used `pickle` for serializing and deserializing cache data to/from disk, which is vulnerable to insecure deserialization (arbitrary code execution if a cache file is maliciously modified).
**Learning:** `pickle` was likely chosen for convenience, but it is inherently unsafe for data that might be modified externally or across trust boundaries. Replacing it with `json` provides a secure alternative for standard data structures.
**Prevention:** Always use secure serialization formats like `json` instead of `pickle` unless dealing with trusted, internally generated complex objects where `pickle` is strictly required and appropriately secured.
