## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.
## 2026-02-24 - XSS in HTML Report Generation
**Vulnerability:** XSS vulnerability found in `generate_report.py` when creating HTML dynamically using f-strings and unsanitized API data.
**Learning:** Directly injecting API data into HTML templates without proper encoding (like `html.escape()`) and URL validation can lead to XSS, particularly when using `javascript:` schemes in `href` links or `onerror` in image `src` attributes.
**Prevention:** Always use `html.escape()` for text data embedded in HTML and strictly validate URLs to ensure they use allowed schemas (e.g. `http://`, `https://`) before using them in links or images.
## 2026-02-24 - API Response NoneType Vulnerabilities
**Vulnerability:** Calling `html.escape(None)` or `.startswith()` on API data that is explicitly returned as `None` causes a `TypeError` application crash.
**Learning:** Using `.get('key', 'default')` is insufficient if the API explicitly returns `None` for a key, because `None` overrides the default parameter.
**Prevention:** Always use a helper function (like `def esc(val, default="")`) that handles `None` checks, and use the `or` operator (e.g. `item.get('url') or 'fallback'`) to enforce defaults when values are `None`.
