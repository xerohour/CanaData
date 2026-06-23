## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-06-23 - Insecure Deserialization in CacheManager
**Vulnerability:** The cache manager was using `pickle` to deserialize objects from disk (`test_cache/....cache`). `pickle` is unsafe when loading files from untrusted sources, potentially leading to Remote Code Execution (RCE).
**Learning:** The cache manager stored API requests to the disk cache. These files could be modified by an attacker. When `pickle.load` deserialized it, code execution could occur.
**Prevention:** Replace `pickle` with `json` (or another safe serialization format like MessagePack if binary size matters). Add backwards compatibility exception handling (catch `json.JSONDecodeError` and `UnicodeDecodeError`) when converting from `pickle` to gracefully discard old binary files.
