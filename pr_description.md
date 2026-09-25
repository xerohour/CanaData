💡 What
We improved the "no results" empty state for client-side search filtering in the interactive dashboard (`CanaParse.py`). It now includes a more polished, visually distinct container and an icon. We also changed the global search input type from `text` to `search` to enable a native clear button in supported browsers.

🎯 Why
When users searched and no results were found, the plain text message lacked the visual polish of the rest of the application. More critically, visually impaired users wouldn't know the table had emptied. Upgrading the input to `type="search"` provides a quick way to clear the filter.

📸 Before/After
Before:
A plain text string "No matching items found in this section." and a standard text input.

After:
A styled glassmorphic container with a decorative emoji, and a native search input with a clear button.

♿ Accessibility
Added `role="status"` and `aria-live="polite"` to the empty state container. This ensures that screen readers announce the empty state dynamically when the search filter removes all listings. We also added `aria-hidden="true"` to the decorative icon within the empty state to prevent clunky screen reader announcements.