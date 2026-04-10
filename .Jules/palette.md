## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2025-04-10 - Screen Reader Verbosity in HTML Reports
**Learning:** Images acting as icons next to text headings (like dispensary avatars next to names) cause screen readers to read the same text twice if the image `alt` text matches the heading.
**Action:** Added `alt=""` and `aria-hidden="true"` to decorative avatars. Also hid emojis and added descriptive `aria-label`s to rating symbols (`★`) to improve screen reader flow.
