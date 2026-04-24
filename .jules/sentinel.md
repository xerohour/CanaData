## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-04-24 - Cross-Site Scripting (XSS) in HTML Reports
**Vulnerability:** Dynamically injected API data (promo codes, URLs, avatars) were not sanitized when constructing HTML via f-strings in `generate_report.py`.
**Learning:** External API data should never be trusted as safe HTML content, even if it comes from an established service.
**Prevention:** Always explicitly sanitize all dynamic data using `html.escape()` before injecting it into HTML templates.
