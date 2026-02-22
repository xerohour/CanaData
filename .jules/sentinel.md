## 2026-02-22 - Path Traversal in File Exports
**Vulnerability:** Path traversal vulnerability in `csv_maker` function in `CanaData.py` allowing arbitrary file writes via malicious filenames.
**Learning:** The application took user input (search slug) and directly used it to construct file paths without sanitization, assuming input would be safe.
**Prevention:** Implemented strict whitelist-based filename sanitization using regex `[^a-zA-Z0-9_\-\.]` to strip directory traversal sequences and unsafe characters before file creation.
