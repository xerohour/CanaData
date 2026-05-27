## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2024-05-18 - External Link Indicators
**Learning:** Links that open in a new tab (`target="_blank"`) without visual and screen-reader indication create a disorienting experience, especially for users relying on assistive technologies or who expect links to replace the current view.
**Action:** Added an inline SVG external link icon (with `aria-hidden="true"`) to "View on Weedmaps" buttons and appended `(opens in a new tab)` to the `aria-label`. Ensured flexbox alignment so the icon sits neatly next to text.
