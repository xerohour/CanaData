## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.
## 2026-07-12 - Skip Link Target Accessibility
**Learning:** Target elements of skip links (like `<div id="main-content">`) must have `tabindex="-1"` so they can programmatically receive focus, otherwise keyboard focus doesn't correctly transfer to the main content area.
**Action:** Added `tabindex="-1"` to the `#main-content` container in `generate_report.py`. Always include this attribute on skip link targets to ensure proper keyboard navigation.
