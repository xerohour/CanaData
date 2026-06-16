## 2026-06-16 - Add Alt Text to Images in HTML Report
**Learning:** Images displayed in the generated HTML dashboard (CanaParse) lack the `alt` attribute for accessibility. This makes it impossible for screen reader users to identify the product imagery shown.
**Action:** When using the `yattag` library to generate image tags (`doc.stag('img', ...)`), always include a descriptive `alt` attribute that provides context for the image, such as the product name or category.
