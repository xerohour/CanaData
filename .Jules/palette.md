## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-05-15 - Semantic Landmarks and Redundant Alt Text
**Learning:** Using `div` targets for skip-links fails programmatic focus unless `tabindex="-1"` is added. In addition, avatar images immediately preceding identical text headings create redundant screen reader announcements.
**Action:** Converted the main container to `<main tabindex="-1">` for skip-links and added `alt="" aria-hidden="true"` to decorative avatars to streamline screen reader flow.
