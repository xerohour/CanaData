## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2025-02-18 - Screen Reader Redundancy & Skip Link Focus
**Learning:** Structural skip-link targets (like `<main>`) require `tabindex="-1"` to properly receive programmatic focus from Playwright/screen readers, and decorative images adjacent to identical heading text cause redundant, annoying screen reader announcements.
**Action:** Always use `<main tabindex="-1">` for skip-link targets and apply `alt="" aria-hidden="true"` to decorative images that immediately precede heading text.
