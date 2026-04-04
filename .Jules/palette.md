## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-04 - Helpful Empty State for Discovery Report
**Learning:** A blank page when no search results are found creates a confusing experience. Users might think the application is broken or still loading.
**Action:** Added a helpful empty state to `generate_report.py` when `listings` is empty. The empty state includes a clear message, a friendly icon, and suggests trying different search parameters, improving overall UX and providing clear feedback.
