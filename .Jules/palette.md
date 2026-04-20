## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.
## 2025-04-20 - Semantic HTML Landmarks and Table Accessibility
**Learning:** The dynamically generated HTML report lacked semantic landmarks for the main content area and incorrectly used `<td>` for row labels in data tables, negatively impacting screen reader navigation and data association. Using `<div>` for the main wrapper and `<td>` for headers fails to convey document structure to assistive technologies.
**Action:** Replace the primary `<div id="main-content">` wrapper with `<main id="main-content">` and change table row labels from `<td class="label">` to `<th scope="row" class="label">`, updating associated CSS to ensure visual consistency while drastically improving semantic accessibility.
