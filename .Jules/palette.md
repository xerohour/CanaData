## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2024-05-04 - Screen Reader Image Redundancy & Skip-Link Target Focus
**Learning:** Using the identical text for an image's `alt` attribute and the adjacent heading causes screen readers to announce the same text twice unnecessarily. Also, skip links require their target to have `tabindex="-1"` (and ideally use semantic landmark tags like `<main>`) to receive programmatic focus correctly.
**Action:** Used `alt="" aria-hidden="true"` on decorative avatars next to identical headings to mute redundant announcements. Updated skip-link targets to use `<main tabindex="-1">` to ensure programmatic focus works properly.
