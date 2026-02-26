## 2026-02-26 - Path Traversal in CSV Export
**Vulnerability:** The `csv_maker` method in `CanaData.py` used unsanitized user input (`searchSlug`) to construct file paths for CSV exports. This allowed attackers to write files to arbitrary locations by supplying path traversal characters (e.g., `../`).
**Learning:** Functions that perform file operations based on user input must sanitize the filename to ensure it remains within the intended directory. Relying on implicit assumptions about input format is dangerous.
**Prevention:** Implement strict input sanitization using `os.path.basename` to strip directory components and an allowlist (e.g., regex `[^a-zA-Z0-9_-]`) for characters.
