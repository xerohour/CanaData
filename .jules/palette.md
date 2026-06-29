## 2026-06-28 - Missing Search Input Label
**Learning:** Found an input element without an associated label or `aria-label` which breaks accessibility for screen reader users trying to use the search functionality.
**Action:** When working with dynamic input fields, always supply an `aria-label` attribute if a standard label isn't used.
