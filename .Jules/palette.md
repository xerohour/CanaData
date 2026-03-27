## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2024-05-24 - Redundant Screen Reader Announcements
**Learning:** Avatars directly preceding headings with the exact same text cause redundant screen reader announcements in generated HTML reports.
**Action:** Always mark such images as decorative (`alt="" aria-hidden="true"`) to improve the screen reader experience.
