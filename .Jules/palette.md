## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-05-29 - Clickable Phone Numbers in HTML Reports
**Learning:** Business phone numbers were rendered as unclickable text in the generated HTML reports, creating friction for users who had to manually copy/paste them into their dialer.
**Action:** Wrapped the phone numbers in standard `<a href="tel:...">` tags with a dedicated `.phone-link` class and added an explicit `aria-label` for screen reader clarity.
