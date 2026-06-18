## 2026-06-18 - Added Aria Labels to Generated Images
**Learning:** In dynamically generated HTML reports (like those created via `yattag`), static images often miss critical `alt` text, and wrapped image links often lack descriptive `aria-labels`. Extracting dynamic values (like product names) ensures screen readers don't just announce 'link'.
**Action:** Always verify that dynamically built HTML tags containing interactive elements or media include `alt` or `aria-label` attributes derived from the surrounding context or payload.
