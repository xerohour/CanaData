## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.
## 2026-03-15 - Enhance generated HTML report accessibility
**Learning:** Using generic `<div>` containers as target links for `skip-to-content` functionality degrades screen reader experience, and empty data lists without defined `role="status"` elements fail to announce state to assistive technology.
**Action:** Use semantic `<main>` tags for the primary content wrapper to properly support skip-links. Additionally, dynamically render an empty state element with `role="status"` and the `.empty-state` CSS class when list arrays (like `listings`) are empty to ensure assistive technologies announce the updated interface correctly.
