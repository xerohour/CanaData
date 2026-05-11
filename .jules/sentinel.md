## 2024-05-11 - Comprehensive XSS Sink Audit in HTML Generation
**Vulnerability:** Multiple Cross-Site Scripting (XSS) vulnerabilities found in `generate_report.py` across different attributes (href, src) and text nodes (`region_name`, `total_listings`, `promo_code`).
**Learning:** When generating HTML via manual string interpolation, developers often escape the primary variables but neglect secondary data points like URLs, promo details, and aggregate metrics. Fixing just one sink leaves the others exposed.
**Prevention:** Perform a comprehensive audit of all dynamic variables in the same context whenever a string interpolation vulnerability is discovered. Always apply consistent escaping to all external or user-controlled inputs.
