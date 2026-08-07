## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2026-04-15 - HTML Report Empty State
**Learning:** Generating empty grids without feedback leaves users wondering if the report is broken.
**Action:** Added an explicit, visually distinct `.empty-state` container with an icon (using `aria-hidden="true"`) and helpful guidance when zero listings are found.

## 2026-07-19 - Skip Link Target Focus
**Learning:** Skip links require the target container to have `tabindex="-1"`. Without this, the browser scrolls to the container but keyboard focus is not programmatically moved, breaking keyboard navigation flow.
**Action:** Always add `tabindex="-1"` to the target element of a skip-to-content link to ensure focus is properly set when the link is activated.
## 2026-07-24 - Emoji Icons as Decorative Elements
**Learning:** The portal uses large emojis as decorative visual icons in cards. Without `aria-hidden="true"`, screen readers read these out before the actual card heading (e.g., "bar chart, Interactive Dashboard"), which creates a clunky and confusing navigation experience.
**Action:** Always add `aria-hidden="true"` to emoji-based decorative structural icons across the application to keep screen reader flow clean and focused on the actual content.
## 2026-07-29 - [Added Keyboard Navigation and Focus Visible to Table Headers]
**Learning:** Table headers used for sorting need explicit focus indicators and keyboard event handling to be accessible to keyboard users.
**Action:** Always add tabindex="0", role="button", and keydown event listeners (for Enter and Space keys) to interactive table headers, along with a *:focus-visible style for clear visual focus.

## 2026-08-01 - Accessible Smooth Scrolling
**Learning:** Anchor links (like skip links or nav menus) cause abrupt page jumps. Smooth scrolling improves UX, but must be paired with prefers-reduced-motion to respect users with vestibular disorders.
**Action:** Always wrap smooth scrolling behavior in a @media (prefers-reduced-motion: no-preference) query.
