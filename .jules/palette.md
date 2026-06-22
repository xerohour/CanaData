
## 2026-06-22 - Add ARIA Labels and Alt Text to Product Gallery Thumbnails
**Learning:** The dashboard generates image gallery links via the `yattag` library without contextual `alt` text or `aria-label`s. This makes it impossible for screen readers to describe the product images or the purpose of the zoom link. Passing attributes containing hyphens in `yattag` requires tuple positional arguments (e.g., `('aria-label', val)`).
**Action:** When dynamically rendering HTML tables containing media, ensure that every `img` tag receives a contextual `alt` attribute and wrapping action links (like lightbox zooms) receive descriptive `aria-label` attributes using available row data (e.g., product names).
