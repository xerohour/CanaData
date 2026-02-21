## 2026-02-21 - [Path Traversal in CSV Export]
**Vulnerability:** User-controlled input (`searchSlug`) was used directly in file paths for CSV export, allowing arbitrary file write via path traversal (`../`).
**Learning:** `CanaData` relies heavily on `searchSlug` for both API queries and filenames. Sanitization requirements differ: URL encoding for API, strict character allow-listing for filesystem.
**Prevention:** Implemented `_sanitize_filename` helper in `CanaData` class that uses `os.path.basename` and regex allow-list. All file operations using user input must pass through this sanitizer. Also applied URL encoding to API parameters.
