
## 2026-02-18 - Missing ARIA attributes and Title in dynamic HTML
**Learning:** Dynamically generated HTML reports using `yattag` can often omit crucial accessibility elements like `<title>` tags and `alt`/`aria-label` attributes on dynamically created links and images. Specifically, adding multiple attributes with hyphens (like `aria-label`) requires passing them as positional tuples inside the `tag` method when using `yattag`.
**Action:** Always check the code generation logic for static or dynamic reports and ensure semantic HTML tags and proper ARIA labels are constructed programmatically. Use positional tuples in `yattag` for hyphenated attributes.
