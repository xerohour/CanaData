## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-07-19 - Skip Link Target Focus
**Learning:** Skip links require the target container to have `tabindex="-1"`. Without this, the browser scrolls to the container but keyboard focus is not programmatically moved, breaking keyboard navigation flow.
**Action:** Always add `tabindex="-1"` to the target element of a skip-to-content link to ensure focus is properly set when the link is activated.

## 2026-07-21 - Portal Index Accessibility Polish
**Learning:** The root index portal lacked visible focus states and had decorative emojis that were being read out by screen readers.
**Action:** Always include `:focus-visible` styles for keyboard accessibility, use semantic `<main>` tags for content wrappers, and explicitly hide decorative icons with `aria-hidden="true"`.
