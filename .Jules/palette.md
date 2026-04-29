## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2024-04-29 - Skip-Link Focus and Redundant Alt Text
**Learning:** Skip-link targets require `tabindex="-1"` to properly receive programmatic focus across all browsers, otherwise the focus order is not correctly updated for keyboard navigation. Additionally, images immediately preceding text containing the identical name create redundant screen reader announcements.
**Action:** Always use `<main tabindex="-1">` for primary skip-link targets and apply `alt="" aria-hidden="true"` to purely decorative or redundant avatar images next to descriptive headings.
