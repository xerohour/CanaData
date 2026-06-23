## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-02-28 - [CRITICAL] Fix insecure pickle deserialization vulnerability
**Vulnerability:** Found `pickle.load` being used on files retrieved from disk without prior authentication/verification, leading to arbitrary code execution (RCE) via insecure deserialization.
**Learning:** Legacy caching mechanisms often rely on `pickle` for convenience despite the widely documented security risks. When modernizing caching layers, always ensure explicit handling of legacy cache files (e.g., catching `UnicodeDecodeError` when shifting from binary to text).
**Prevention:** Use safer serialization formats like `json` by default. If complex object serialization is strictly required, validate payloads cryptographically using HMAC signatures before deserialization or use safer alternatives like `msgpack`.
