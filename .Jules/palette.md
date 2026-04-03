## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-03 - Redundant Alt Text on Avatars
**Learning:** Avatars preceding headings with identical text (like the dispensary names in `generate_report.py`) cause redundant screen reader announcements.
**Action:** Marked such avatars as decorative (`alt="" aria-hidden="true"`) to improve accessibility.
