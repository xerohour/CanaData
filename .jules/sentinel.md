## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - HTML Injection (XSS) in HTML Report Generator
**Vulnerability:** Untrusted string values fetched from Weedmaps API (e.g. location names, urls, and promo code strings) were dynamically injected into an HTML report via f-strings without escaping in `generate_report.py`.
**Learning:** Using raw f-strings for templating dynamically introduces severe cross-site scripting (XSS) risks when handling external payloads, as they natively evaluate user input as syntax.
**Prevention:** Always serialize and string-escape variables before dropping them into raw HTML structures. Use built-in libraries such as `html.escape` and ensure strict typing to prevent tracebacks.
