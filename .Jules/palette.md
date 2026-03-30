## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2024-03-30 - Decorative Avatar Accessibility
**Learning:** The `generate_report.py` file previously used the listing's name for both the avatar image `alt` text and the adjacent `<h2>` heading. This causes screen readers to redundantly announce the name twice.
**Action:** When an image directly precedes a heading containing the exact same text, mark the image as decorative (`alt="" aria-hidden="true"`) to prevent redundant announcements.
