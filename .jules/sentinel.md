## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-25 - XSS via Unescaped API Data in f-strings
**Vulnerability:** The HTML report generator `generate_report.py` was vulnerable to Cross-Site Scripting (XSS). It used raw f-strings to inject unverified API data (names, cities, promos) directly into HTML without sanitization, and didn't validate URL schemas for links.
**Learning:** Even internal reporting tools can be vectors for XSS if they reflect untrusted data (like API responses) into HTML without using an auto-escaping templating engine or manually escaping. URL parameters must also be validated to prevent `javascript:` schemas.
**Prevention:** Always explicitly use `html.escape()` when formatting HTML with raw f-strings. Validate URL schemas (e.g., checking for `http`/`https` protocols) before injecting them into `href` or `src` attributes.
