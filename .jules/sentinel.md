## 2026-02-20 - [Input Sanitization in URL Construction]
**Vulnerability:** Unsanitized user input (`searchSlug`) was concatenated directly into API URLs in `CanaData.py`.
**Learning:** `CanaData.py` constructs URLs manually using f-strings, which is vulnerable to parameter injection if the input contains `&` or other special characters. `requests` does not auto-encode these when passed as part of the URL string.
**Prevention:** Use `urllib.parse.quote` to sanitize inputs before concatenation, or use the `params` dictionary argument in `requests.get` (though this would require a larger refactor of `do_request` here).
