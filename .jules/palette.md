## 2024-05-16 - Dynamic Alt Text and ARIA Labels for Generated HTML
**Learning:** When generating static HTML for data grids (like the CanaData dashboard), generic accessibility tags (e.g. `alt="product image"`) provide insufficient context for screen readers traversing long lists.
**Action:** Always extract contextual data from the adjacent row (e.g., `row[2]` for product name) to generate specific `alt` text (e.g., `alt="Thumbnail of {product_name}"`) and descriptive `aria-label` attributes on interactive link wrappers.
