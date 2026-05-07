## 2024-05-07 - Incomplete Contextual Escaping in HTML Generation
**Vulnerability:** Multiple Cross-Site Scripting (XSS) sinks in HTML report generation (avatar URLs, web URLs, promo text, empty state region).
**Learning:** When performing manual string interpolation for HTML generation, developers often remember to escape primary data fields but frequently overlook secondary fields like URLs (`href`, `src`), promotional content, and empty-state placeholders.
**Prevention:** Perform a comprehensive audit of ALL dynamic variables within the same context when fixing manual HTML string interpolation. Ensure proper escaping for all attributes and secondary content fields.
