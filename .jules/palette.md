## 2024-07-13 - Focus management for skip links
**Learning:** When implementing 'skip to main content' accessibility links, the target container element must explicitly include the tabindex="-1" attribute. This is required for the container to programmatically receive keyboard focus when the anchor link is activated.
**Action:** Always add tabindex="-1" to the target element of skip links.
