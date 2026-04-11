## 2024-04-11 - XSS in HTML Report Generator
**Vulnerability:** Untrusted dictionary values from API/scraped JSON were injected directly into an HTML string via f-strings without any escaping. In addition, URLs like `web_url` and `avatar` lacked scheme validation, opening vectors for `javascript:` URIs.
**Learning:** Raw f-strings are highly dangerous for generating HTML from external data because they lack the automatic contextual escaping provided by modern templating engines (like Jinja2).
**Prevention:** Always manually apply `html.escape()` to text nodes and validate protocol schemes (`http://`, `https://`) for URL attributes when generating raw HTML strings. Consider using a templating engine.
