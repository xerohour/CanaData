
## 2024-06-26 - A11y Context for Shorthand Values
**Learning:** Screen readers struggle with shorthand text like "★ 4.5 (100)", reading it literally which confuses users. Similarly, external links without warnings disorient screen reader users when a new tab opens unexpectedly.
**Action:** Always use `aria-label` and `title` attributes on shorthand badges to provide full context (e.g., "Rating: 4.5 stars, 100 reviews") and append "(opens in a new tab)" to external link `aria-labels`.
