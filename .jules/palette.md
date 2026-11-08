## 2026-10-07 - Dynamic DOM Accessibility & Decorative Emojis
**Learning:** Purely decorative emojis in empty states need `<span aria-hidden="true">` to prevent screen reader noise. When using client-side JavaScript to mutate tables dynamically (filtering/sorting/pagination), screen readers do not automatically announce the state changes or results, and visual `disabled` buttons still remain keyboard-navigable without `aria-disabled="true"`.
**Action:** Always inject an `aria-live="polite"` region to announce dynamic JavaScript search/sort results, wrap purely visual decorative emojis in `aria-hidden="true"`, and apply `aria-disabled="true"` to visually disabled interactive elements so they are correctly communicated to assistive technologies.
## 2026-11-02 - Semantic Landmarks and Redundant Image Announcements
**Learning:** When images immediately precede text containing the exact same information (like a product name or avatar next to a heading), screen readers will redundantly read the text twice. Additionally, screen readers need semantic HTML5 landmarks like `<main>` to navigate effectively.
**Action:** Use `alt="" aria-hidden="true"` on redundant images when the adjacent text already provides the context, and always wrap the primary content of a page in a `<main>` tag instead of a generic `<div id="main-content">`.

## 2026-11-07 - Accessible External Links
**Learning:** External links (`target="_blank"`) without visual indicators or accessible names confuse users, particularly screen reader users, when the link abruptly opens a new tab.
**Action:** Always append `(opens in a new tab)` to the `aria-label` or accessible name of an external link, and provide a visual indicator (like an SVG icon) to prepare sighted users.
