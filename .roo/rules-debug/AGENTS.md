# AGENTS.md (Debug Mode)

- 503 errors during menu scraping often indicate the menu is too large for the Weedmaps API to return in a single JSON blob.
- "First Byte error" (503) in `CanaData.py` is caught and skipped; check the URL in a browser for more details.
- Use `-tshoot` flag with `CanaData.py` to enable more verbose logging of API URLs.
- If CSV parsing fails with "list index out of range", it typically means the source CSV is empty or has fewer columns than expected by the parser's hardcoded indices.
