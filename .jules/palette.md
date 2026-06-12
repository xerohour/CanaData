
## 2026-06-12 - Product Image Accessibility in Generated Tables
**Learning:** Product thumbnails in the generated HTML table (CanaParse.py) lacked `alt` attributes and the surrounding Fancybox links lacked `aria-labels`. This made the product grid largely inaccessible to screen reader users, who couldn't identify the visual content or the purpose of the image link.
**Action:** Added dynamic `alt` and `aria-label` attributes using the product's name (parsed from the row data). Always ensure image links and thumbnails in generated content have contextual, descriptive labels.
