## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2025-04-08 - Fix XSS Vulnerability in HTML Report Generation
**Vulnerability:** The script `generate_report.py` dynamically builds an HTML file (`listing_report.html`) using raw f-strings without escaping variables extracted from the external API (like item name, address, promos). This exposes the application to Cross-Site Scripting (XSS) if the API returns malicious HTML payloads.
**Learning:** Using raw f-strings without an auto-escaping templating engine like Jinja2 easily leads to HTML injection vulnerabilities. Additionally, checking for URL protocols is crucial to prevent `javascript:` payloads in link tags.
**Prevention:** Always explicitly use `html.escape()` when constructing HTML directly from strings, or use a templating engine that handles auto-escaping. Also, validate that URLs begin with safe protocols (`http`/`https`).
