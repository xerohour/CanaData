## 2026-06-04 - Adding ARIA labels and Alt Text to generated HTML output
**Learning:** When generating static HTML artifacts dynamically (e.g., via yattag), it's critical to weave accessibility attributes (like `alt` text and `aria-label`s) directly into the generator functions to ensure consistent accessibility across all generated rows, rather than trying to modify the static output later.
**Action:** When adding attributes with hyphens (like `aria-label`) in `yattag`, pass them as tuples and always position them before keyword arguments like `href=` to avoid Python `SyntaxError`s.
