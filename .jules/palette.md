
## 2024-11-20 - Dynamic Image Accessibility
**Learning:** Dynamically generated images and their parent links in the `yattag` HTML report lacked contextual accessibility attributes, causing screen readers to read raw URLs instead of the product names.
**Action:** Added `alt` and `aria-label` attributes using the row data (e.g., product name) to dynamically provide context.
