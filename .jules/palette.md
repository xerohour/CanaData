## 2026-06-07 - Add accessibility attributes to dynamically generated images
**Learning:** Automatically generated HTML dashboards from CSV data often neglect accessibility, particularly screen-reader friendly `alt` text and `aria-label`s on images that users interact with. Adding these dynamically using available context (like product names) ensures the output remains accessible regardless of the dataset.
**Action:** Always map relevant textual data (e.g., product names or titles) to `alt` and `aria-label` attributes when dynamically rendering image elements or interactive wrappers.
