## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2025-04-25 - XSS Vulnerability in HTML Report Generation
**Vulnerability:** Unsanitized dynamic data from external APIs (promo codes, avatar URLs, external links, and region names) were directly interpolated into an HTML string in `generate_report.py`, leading to Cross-Site Scripting (XSS) risks.
**Learning:** Even when generating static HTML files locally or from trusted data sources like Weedmaps, any externally sourced string must be properly sanitized, as API payloads could contain malicious inputs.
**Prevention:** Always use `html.escape()` when injecting dynamic text or attributes into HTML via string formatting. For URLs, additionally ensure they are properly encoded.
