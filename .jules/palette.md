## 2024-07-16 - Skip-to-content focus management
**Learning:** Target container elements for 'skip to main content' links (like <div id="main-content">) must explicitly include the tabindex="-1" attribute to programmatically receive keyboard focus when the anchor link is activated.
**Action:** Always ensure target elements for internal anchor links have tabindex="-1" if they are not natively focusable elements to maintain correct keyboard navigation flow.
