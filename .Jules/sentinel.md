## 2025-05-08 - [Missing Escaping in Manual HTML Interpolation]
**Vulnerability:** [Multiple XSS sinks found in generate_report.py where dynamic data (promo details, avatar URLs, web URLs, empty state parameters) were interpolated into HTML without escaping.]
**Learning:** [When fixing an identified XSS vulnerability, a comprehensive audit must be performed because multiple similar sinks often exist alongside the specifically reported one in the same context.]
**Prevention:** [Always wrap dynamic data in html.escape(str(var)) when performing manual string interpolation to generate HTML, especially for URLs and deeply nested dictionary attributes.]
