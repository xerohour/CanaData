## 2024-05-09 - Fix XSS in Promo Fields
**Vulnerability:** XSS vulnerability in generate_report.py where promo code and title fields were unescaped.
**Learning:** Manual string interpolation for generating HTML misses sanitization easily on nested dict fields (like promos), unlike template engines which often auto-escape.
**Prevention:** Ensure all dynamic user or API-controlled variables are wrapped in html.escape(str()) before string formatting into HTML blocks.
