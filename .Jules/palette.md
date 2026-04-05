## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.
## 2026-02-24 - Zero-Data States
**Learning:** Users lack feedback when an API request successfully returns zero listings, resulting in a blank page below the header that appears broken.
**Action:** Implemented a visual empty state with a helpful icon and explanation message in the report generator to provide clear feedback during zero-results scenarios.
