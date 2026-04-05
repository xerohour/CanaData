## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - Cross-Site Scripting (XSS) in HTML Generation
**Vulnerability:** Raw string formatting (`f-strings`) without HTML escaping in `generate_report.py` created XSS vulnerabilities when inserting user-controlled API data into the DOM. URL attributes like `src` and `href` were also vulnerable to `javascript:` payload injections.
**Learning:** When writing raw HTML strings directly instead of using templating engines like Jinja2 or Yattag (which handle auto-escaping), developers must manually escape all dynamic variables using `html.escape()`.
**Prevention:** Always use `html.escape()` when inserting untrusted data into HTML. For URLs in `src` or `href` attributes, validate the schema strictly allows only `http` or `https` to prevent script execution.
