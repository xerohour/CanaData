## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.
## 2024-04-24 - Semantic Landmarks and Scope for Screen Readers
**Learning:** Generating HTML reports without semantic landmarks (`<main>`) or row headers (`<th scope="row">` for `td.label`) prevents screen readers from correctly navigating the content and associating data rows.
**Action:** Use the `<main>` tag for primary content areas and apply `<th scope="row">` to the leftmost identifying cells of data tables. Adjust associated CSS to target `th` instead of just `td` to maintain visual consistency.
