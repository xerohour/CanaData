## 2024-07-17 - Skip Link Focus Accessibility
**Learning:** Target container elements for "skip to main content" links must explicitly include tabindex="-1" to correctly receive programmatic keyboard focus. Standard div elements do not receive focus by default.
**Action:** When implementing skip links, ensure the target element has tabindex="-1".
