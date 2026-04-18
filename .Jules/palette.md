## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-05-18 - External Link Accessibility
**Learning:** External links (`target="_blank"`) that open in new tabs can disorient screen reader users if they aren't warned before the context switch occurs. Adding a visual indicator (`↗`) and an explicit aria-label warning improves predictability.
**Action:** Always append " (opens in a new tab)" to the `aria-label` of links with `target="_blank"` and include a screen-reader-hidden visual indicator `<span aria-hidden="true">↗</span>` to inform sighted users.
