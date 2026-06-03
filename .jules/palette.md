## 2024-05-24 - Initial Journal
**Learning:** Initial Palette journal created.
**Action:** Ready for UX improvements.
## 2024-05-24 - Accessible Images and Empty States in generated HTML
**Learning:** When using Python HTML generators like Yattag, it's easy to overlook screen reader accessibility for dynamic tabular data. Using empty table rows or simple text can be visually confusing. Furthermore, decorative elements inside interactive anchors must have descriptive ARIA labels to provide context for screen reader users traversing galleries.
**Action:** Always include dynamically generated `alt` text for images (e.g. product names) and `aria-label`s on their parent anchor tags for gallery links. Use visually distinct, styled "empty state" components instead of plain text to improve the user experience when filters return no results.
