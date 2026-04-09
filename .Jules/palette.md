## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.
## 2026-04-09 - Empty State HTML Reports
**Learning:** HTML reports without listings look broken or empty without an explicit visual signal.
**Action:** Always include a `.empty-state` div to provide helpful feedback when the listings array is empty. Added `aria-hidden="true"` to the decorative icon to prevent screen reader noise.
