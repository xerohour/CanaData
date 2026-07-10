## 2026-06-28 - Preventing XSS via javascript: URI in dynamically generated hrefs
**Vulnerability:** HTML reports dynamically construct `href` attributes for Weedmaps links from external JSON fields (e.g., `item.get('web_url')`). Although `html.escape()` is used, it fails to sanitize `javascript:` URIs, leading to a critical XSS vulnerability when a user clicks the link.
**Learning:** `html.escape()` is insufficient for `href` attributes because the context allows protocol-based execution (`javascript:` or `data:`).
**Prevention:** Implement explicit protocol validation for `href` attributes (allowing only safe protocols like `http://` and `https://`), enforce this using a helper function, and implement a strict Content-Security-Policy (CSP) as defense-in-depth.
