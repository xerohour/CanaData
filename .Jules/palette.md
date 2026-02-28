## 2025-02-28 - Descriptive ARIA labels for repeating actions
**Learning:** In list or grid views (like the discovery report), repeating "View Details" or "View on Weedmaps" buttons create poor screen reader experiences because the text lacks context without visually associating it with the card title.
**Action:** Always append an `aria-label` attribute (e.g., `aria-label="View {item_name} on Weedmaps"`) to generic action buttons/links within mapped or repeating UI patterns.
