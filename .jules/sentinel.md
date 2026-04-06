## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Cross-Site Scripting (XSS) in HTML Report Generator
**Vulnerability:** Unescaped JSON data interpolated directly into raw f-strings in `generate_report.py` allowed XSS via malicious API responses.
**Learning:** When manually constructing HTML without a templating engine (like Jinja2), all dynamic values, especially those sourced from external APIs, must be explicitly escaped. URL fields are particularly dangerous as they can host `javascript:` payloads.
**Prevention:** Always use `html.escape()` on string interpolation in HTML generation scripts, and strictly validate URL schemas to ensure they use safe protocols (`http`/`https`).
