## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-03-31 - [Insecure Deserialization via pickle in CacheManager]
**Vulnerability:** The CacheManager used `pickle` for disk caching, leading to arbitrary code execution if a malicious `.cache` file was placed in the cache directory.
**Learning:** Using `pickle` for caching any data, even data presumed to be internal, is dangerous because it inherently allows arbitrary object instantiation and code execution upon deserialization. The filesystem is an untrusted boundary.
**Prevention:** Always use safe serialization formats like `json` for caching or data exchange unless executing Python objects is an explicit, intensely secured requirement. Handled `UnicodeDecodeError` and `json.JSONDecodeError` to gracefully fail on legacy pickle files.
