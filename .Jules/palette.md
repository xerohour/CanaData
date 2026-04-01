## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.
## 2024-04-01 - Redundant Screen Reader Announcements
**Learning:** When an image (like an avatar) directly precedes a heading containing the exact same text, screen readers will announce the text twice if the image has alt text matching the heading.
**Action:** Mark the image as decorative (`alt="" aria-hidden="true"`) to prevent redundant screen reader announcements.
