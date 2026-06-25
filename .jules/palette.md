## 2026-06-25 - Add Skip to Content Link to CanaParse Dashboard
**Learning:** Legacy generated HTML dashboards often overlook basic keyboard navigation, prioritizing visual structure (`.container-fluid main`) over screen-reader accessibility. Incorporating an invisible, focusable skip link improves keyboard usability significantly for data-heavy pages.
**Action:** When migrating or updating HTML report generators, automatically include a `skip-link` immediately after the `<body>` tag linked to the primary content container ID.
