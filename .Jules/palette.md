## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.
## 2026-03-24 - Screen Reader Redundancy in Listing Cards
**Learning:** Avatars preceding headings with identical text caused redundant screen reader announcements. Using `<main>` instead of `<div>` for the main content container improves ARIA landmark navigation.
**Action:** Marked avatar images as decorative (`alt="" aria-hidden="true"`) and updated the main container to a semantic `<main>` tag in `generate_report.py`.
