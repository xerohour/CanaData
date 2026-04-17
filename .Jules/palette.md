## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2024-05-18 - Decorative vs Informative Images
**Learning:** Images (like store avatars) placed immediately preceding a heading with the exact same text cause screen readers to announce the text twice, creating a stuttering UX.
**Action:** When an image's `alt` text is fully visible in immediately adjacent text, treat the image as decorative by using `alt="" aria-hidden="true"`.
