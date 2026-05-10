## 2026-05-10 - XSS in HTML Report Dynamic Variables
**Vulnerability:** Cross-Site Scripting (XSS) via unescaped dynamic variables (avatar URLs, web URLs, promo details, region_name) in `generate_report.py`.
**Learning:** When string interpolation is used to generate HTML content, all external or user-controlled variables must be explicitly escaped, as similar sinks often exist alongside previously reported ones.
**Prevention:** Consistently apply `html.escape(str(var))` to all dynamic variables rendered in HTML templates to prevent arbitrary script execution.
