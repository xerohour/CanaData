## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-03-01 - Redundant Screen Reader Text in Data Grids
**Learning:** Using the item's name as the `alt` text for its avatar when the name is already the primary heading (`<h2>`) causes screen readers to redundantly announce the name twice. Additionally, raw symbols like "★ 4.9 (350)" are read character-by-character, confusing users.
**Action:** Set decorative or redundant avatar images to `alt="" aria-hidden="true"`. For icon-heavy badges (like ratings), wrap the visual text in `aria-hidden="true"` and provide the full context using `aria-label` and `title` on the parent container.
