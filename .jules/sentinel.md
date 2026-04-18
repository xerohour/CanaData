## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-04-18 - XSS Vulnerability in HTML Generator
**Vulnerability:** Raw f-strings were used to build an HTML file without sanitizing dynamic API data (promo codes, avatars, region names), leading to potential Cross-Site Scripting (XSS).
**Learning:** Even internal reporting tools are vulnerable if they reflect external API data into the DOM without escaping.
**Prevention:** Always use `html.escape(str(val))` for all dynamic data injections when generating HTML without a templating engine.
