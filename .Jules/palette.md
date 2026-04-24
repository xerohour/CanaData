## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-04-24 - Semantic HTML Landmarks and Table Accessibility
**Learning:** The generated HTML report lacked semantic layout landmarks (like `<main>`) and structural row headers (`<th scope="row">` instead of `<td>` with a label class) for data tables, which impaired screen reader navigation.
**Action:** Converted the primary content div to a `<main>` tag and updated data tables to use `<th scope="row">` for row labels while adjusting CSS to maintain visual consistency.
