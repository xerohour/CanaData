## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2026-02-25 - XSS via Unescaped API Data in Python f-strings
**Vulnerability:** Cross-Site Scripting (XSS) vulnerability found in `generate_report.py` where string data from Weedmaps API (such as location names, types, addresses, and promos) were directly interpolated into an HTML file using f-strings without HTML escaping.
**Learning:** Even when building static HTML offline or locally without a web framework, directly injecting data fetched from third-party APIs into f-strings is a major XSS risk. Furthermore, `javascript:` payload schemas must be mitigated by strictly validating `http://` or `https://` schemas for injected URLs like `avatar_image` and `web_url`.
**Prevention:** Always use standard template engines (like Jinja2) that auto-escape strings, or manually pass interpolated strings through `html.escape()` when rendering HTML with Python f-strings. Enforce schema allowlists for all generated URLs.
