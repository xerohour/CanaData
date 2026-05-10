## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2024-05-10 - HTML Report Data Table Semantics and Image Redundancy
**Learning:** Screen readers struggle with non-semantic grid structures (like basic `<td>` pairs for label/value) and redundantly announce both an image's `alt` text and the adjacent header if they're identical. Also, pure text representation like "★ 4.8 (100)" is visually understood as a rating but sounds confusing to screen readers.
**Action:** Always use `<th scope="row">` for horizontal data labels instead of `<td>` to explicitly bind the label to its value. Use `aria-hidden="true"` and empty `alt` tags on purely decorative or redundant images (like avatars paired with identical `<h2>` titles). Add explicitly descriptive `aria-label` attributes to symbolic data like ratings.
