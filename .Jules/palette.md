## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-03-23 - HTML Report Screen Reader Accessibility
**Learning:** The generated HTML report (`listing_report.html`) included avatar images with full names as alt text directly preceding `<h2>` headings with the same name, causing screen readers to announce the dispensary name redundantly. Additionally, the main content area was wrapped in a generic `<div>` instead of a semantic `<main>` landmark, making the skip link point to a non-landmark region.
**Action:** Replaced the generic `<div>` with a semantic `<main>` tag in `generate_report.py` to improve ARIA keyboard navigation structure. Updated the avatar `<img>` tags to be decorative by setting `alt=""` and `aria-hidden="true"` to prevent redundant screen reader announcements.
