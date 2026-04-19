## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.
## 2026-04-19 - Semantic HTML for Report Accessibility
**Learning:** In static HTML reports, using a standard `<div>` container with an ID for a "skip to main content" link does not provide screen readers with a proper ARIA landmark. Also, data tables utilizing generic `<td>` tags for row labels fail to correctly associate labels with their values for screen readers.
**Action:** Changed the `<div id="main-content">` to a semantic `<main id="main-content">` tag. Updated the report's `.data-table` to use `<th scope="row">` for its label cells. Ensure future HTML generation correctly utilizes semantic tags like `<main>` and `<th>` to create accessible documents out of the box.
