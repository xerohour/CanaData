## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-04-17 - XSS in HTML Report Generation
**Vulnerability:** Unescaped variables (e.g. `promo_code`, `web_url`, `avatar_image`) injected into raw f-strings during HTML generation.
**Learning:** Even internal reporting tools are vulnerable to XSS if they dynamically construct HTML without a templating engine (like Jinja2) and fail to manually sanitize API-derived variables.
**Prevention:** When using raw f-strings to generate HTML, wrap all dynamic data variables with `html.escape(str(val))` before injection to block XSS payloads.
