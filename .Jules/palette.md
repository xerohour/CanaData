## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-05-01 - Redundant Screen Reader Announcements and Skip-Link Targets
**Learning:** Having an image with alt text identical to the adjacent heading causes redundant and annoying screen reader announcements. Additionally, skip-links targeted at non-interactive elements fail to move focus unless the target has `tabindex="-1"`.
**Action:** Always apply `alt="" aria-hidden="true"` to decorative images adjacent to text that conveys the same information. Ensure skip-link targets use a semantic tag like `<main>` and include `tabindex="-1"` to properly receive programmatic focus.
