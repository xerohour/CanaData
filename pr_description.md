🚨 Severity: CRITICAL
💡 Vulnerability: The HTML report generator `parse-script/CanaParse.py` allowed `javascript:` URIs in `href` and `src` attributes by not validating the protocol of URLs, which enables Cross-Site Scripting (XSS).
🎯 Impact: A malicious user could provide a `javascript:` payload in the url and image url of items which would then be executed when clicked on, posing a severe XSS risk.
🔧 Fix: Injected a `isSafeUrl` function to properly check that URL values begin with acceptable protocols (`http://`, `https://`, `#`, `/`) before rendering them. Unsafe image urls fallback to the default avatar and unsafe urls default to `#`.
✅ Verification: Ensure tests pass and verifying the `isSafeUrl` javascript check logic covers `img_url` and `url`.