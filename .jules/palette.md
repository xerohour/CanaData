
## 2026-06-24 - Accessible Gallery Lightboxes
**Learning:** When using gallery libraries like Fancybox wrapping image thumbnails in `<a>` tags, screen readers often read the raw image URL if the link lacks an `aria-label` or the image lacks `alt` text. Passing `aria-label` in `yattag` requires positional tuples like `('aria-label', 'value')` instead of keyword arguments to avoid underscore rendering issues.
**Action:** Always provide explicit, action-oriented `aria-label`s on lightbox links (e.g., "View larger image of [Product]") and descriptive `alt` attributes on the thumbnails inside.
