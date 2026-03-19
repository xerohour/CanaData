## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-03-19 - Dynamic Empty State with Role Status
**Learning:** When searches yield zero results, it's critical to provide an empty state container with role="status" so screen readers announce the lack of results automatically.
**Action:** Implemented a semantic empty state block in generate_report.py. Apply role="status" to all dynamic empty states.
