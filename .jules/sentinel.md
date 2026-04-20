## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-03-05 - XSS Vulnerability in HTML Report
**Vulnerability:** Unsanitized dynamic data injection (promo codes, avatars, URLs) in `generate_report.py` allowed potential Cross-Site Scripting (XSS) via raw f-strings.
**Learning:** Even internal reporting tools must sanitize all data originating from external APIs (like Weedmaps) to prevent script execution when the HTML report is viewed.
**Prevention:** Always use `html.escape()` or a robust templating engine (like Jinja2) when generating HTML with dynamic content, never rely solely on raw f-strings.
