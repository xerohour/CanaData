## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-05-24 - Cross-Site Scripting (XSS) in HTML Report Generator
**Vulnerability:** The HTML report generator (`generate_report.py`) injected external API data (such as `promo_code`, `avatar`, and `region_name`) directly into HTML templates without proper sanitization.
**Learning:** Even deeply nested or optional API fields, and seemingly innocuous input like region names, can be vectors for XSS if they are blindly trusted and rendered in a browser.
**Prevention:** Always sanitize dynamically generated HTML by wrapping any external or user-provided data in `html.escape(str(...))` to ensure HTML entities are properly escaped before injection.
