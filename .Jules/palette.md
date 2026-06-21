## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-06-21 - Image Gallery Accessibility
**Learning:** Thumbnail galleries generated via `yattag` were missing `alt` text and `aria-label`s on their anchor tags, preventing screen reader users from identifying the content of the image lightbox.
**Action:** Always include contextual `alt` text for thumbnails and an `aria-label` on the wrapper anchor tag (e.g. "View [Item] image") when constructing galleries to provide context for visually impaired users.
