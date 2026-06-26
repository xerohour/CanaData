## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2024-05-20 - XSS in HTML Report Generation
**Vulnerability:** Deeply nested fields like promo codes sourced from external APIs were directly interpolated into HTML without escaping.
**Learning:** When dynamically generating HTML, all data sourced from external APIs must be sanitized.
**Prevention:** Always sanitize data using html.escape() to prevent Cross-Site Scripting (XSS) vulnerabilities.
