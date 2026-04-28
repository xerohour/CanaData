## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2025-04-28 - Skip Link Focus & Redundant Image Alt Text
**Learning:** Skip links must target elements that are programmatically focusable. A `<div>` requires `tabindex="-1"` to receive focus without disrupting natural tab order. Also, image alt attributes that merely repeat immediately adjacent heading text create redundant screen reader noise.
**Action:** Ensure structural layout wrappers like `<main>` targeted by skip links have `tabindex="-1"`. Apply `alt="" aria-hidden="true"` to decorative or redundant companion imagery.
