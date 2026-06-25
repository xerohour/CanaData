## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-25 - Unescaped promo codes leading to XSS
**Vulnerability:** XSS vulnerability in HTML report generation due to unescaped external promo data.
**Learning:** When dynamically generating HTML using f-strings, all fields sourced from external APIs must be properly escaped, even deeply nested or optional fields like `promo_code`.
**Prevention:** Always use `html.escape(str(...))` or similar sanitation methods for *any* external string inserted into an HTML template.
