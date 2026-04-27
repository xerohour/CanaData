## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.
## 2024-04-27 - HTML Report Semantic Landmarks and Table Headers
**Learning:** When generating HTML reports, enforcing accessibility requires semantic landmarks (like `<main>`) for primary content areas and `<th scope="row">` for data table row labels. Using generic `<div>` and `<td>` makes it difficult for screen readers to navigate and associate data.
**Action:** Always use `<main>` for primary content linked by skip-links, and use `<th scope="row">` for key-value table structures. Adjust associated CSS to maintain visual consistency when upgrading from generic elements.
