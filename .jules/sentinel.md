## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-03-05 - Fix XSS in HTML report generation
**Vulnerability:** Cross-Site Scripting (XSS) in dynamically generated HTML via f-strings.
**Learning:** Using raw Python f-strings to inject unvalidated/unsanitized data into HTML templates creates critical XSS vulnerabilities. Default parameters (like `.get('key', default)`) don't protect against `None` values or malicious input.
**Prevention:** Always use `html.escape(str(val))` for dynamic HTML content and explicitly validate URL schemas (`http://`, `https://`) to prevent `javascript:` links. Fallback using `or` instead of `.get()` defaults.
