## 2026-05-31 - Missing Alt Text on Product Images
**Learning:** The auto-generated HTML reports for CanaData listings lacked `alt` attributes on product thumbnails and `aria-label`s on their parent anchor links (which trigger a fancybox gallery). Without these, screen readers announce the raw image URL or simply "image" followed by an uninformative link.
**Action:** Always extract the product name (available in `row[2]`) to populate meaningful `alt` text and descriptive `aria-label`s on gallery links in dynamically generated tables.
