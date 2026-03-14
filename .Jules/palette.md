## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.
## 2023-11-09 - Empty States and Semantic Landmarks in Dynamic Reports
**Learning:** When generating dynamic HTML grids (e.g., listing reports), an empty array can lead to a confusing blank page. Adding an explicit empty state with `role="status"` ensures screen readers automatically announce the lack of results. Furthermore, replacing generic wrapper `div`s with semantic `<main>` tags for the primary content container improves skip-link accessibility and landmark navigation.
**Action:** Always implement a stylized empty state with `role="status"` for dynamic data arrays and use semantic HTML tags (`<main>`) for primary content containers targeted by skip-links.
