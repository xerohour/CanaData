## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - XSS in HTML Report Generation
**Vulnerability:** Unescaped strings in nested API fields (`promo_code.code` and `promo_code.title`) were directly injected into an HTML report template.
**Learning:** Even deeply nested and optional API fields must be sanitized when rendering dynamic HTML using Python f-strings.
**Prevention:** Always use `html.escape()` on data sourced from external APIs before injecting it into HTML structures.
