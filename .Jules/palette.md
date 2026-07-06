## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.
## 2026-07-06 - Hidden Focus Links
**Learning:** Screen reader users and keyboard navigators require a "skip link" positioned off-screen that becomes visible upon focus to bypass repetitive navigation header items. Standard interactive elements also require a `:focus-visible` state to show keyboard users where they are without displaying focus rings for mouse users.
**Action:** Added global `*:focus-visible` and `.skip-link` CSS to reports and implemented `<a href="#main-content" class="skip-link">Skip to main content</a>` as the first interactive element.
