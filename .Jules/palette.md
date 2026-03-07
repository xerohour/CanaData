## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-02-24 - Dynamic Grid Empty States
**Learning:** The dynamically generated HTML report displayed a confusing blank grid when the `listings` array was empty, leaving the user without feedback or next steps.
**Action:** Always implement an explicit, stylized empty state (using an `.empty-state` CSS class and descriptive message) when mapping over data arrays to generate visual grid layouts.