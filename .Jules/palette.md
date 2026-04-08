## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-02-24 - Empty States
**Learning:** Missing empty states leave users confused. Generating reports with empty search results resulted in a blank page. Adding a dedicated empty state component with guidance improves user confidence when zero results are returned.
**Action:** Implemented a helpful empty state component in `generate_report.py` to display when no listings match the criteria.
