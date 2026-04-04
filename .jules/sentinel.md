## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Cross-Site Scripting (XSS) in HTML Generation
**Vulnerability:** Unsanitized variables from the Weedmaps API and user input (`region_name`) were directly interpolated into an HTML string in `generate_report.py`, leading to potential XSS.
**Learning:** String interpolation for HTML generation is highly prone to XSS if not handled carefully, even if the data comes from a seemingly trusted 3rd party API.
**Prevention:** Always use an escaping function like `html.escape()` or a templating engine (like Jinja2) that auto-escapes variables when generating HTML from dynamic data. Additionally, validate URLs (e.g. `http/https` check) to prevent `javascript:` links.
