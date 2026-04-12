## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-24 - HTML XSS via Dynamic Template
**Vulnerability:** Raw string formatting (`f-strings`) was used to generate HTML reports from API data without input sanitization, opening up potential Cross-Site Scripting (XSS) via maliciously crafted listing names or region names.
**Learning:** Directly injecting unescaped dict values from external APIs into HTML content is dangerous, even if the data comes from a known API like Weedmaps. The API could return `None`, or an attacker could poison upstream data.
**Prevention:** Always use `html.escape(str(val))` when dynamically injecting values into HTML strings. Ensure a safe fallback with `or` to handle `None` values.
