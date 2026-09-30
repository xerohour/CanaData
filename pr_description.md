💡 What:
- Added `aria-live="polite"` to dynamic pagination text in HTML reports.
- Added `cursor: not-allowed` and `aria-disabled="true"` to disabled navigation buttons.
- Wrapped purely decorative emojis in `<span aria-hidden="true">` across templates.
- Explicitly marked inline noun emojis (e.g., ❤️ for 'love') with `role="img"` and `aria-label`.

🎯 Why:
To ensure reports remain fully accessible to screen readers, dynamic data such as "Showing 1-50 of 300" requires an `aria-live` region so it is announced when changed. Similarly, purely decorative emojis (like sparkles or coffee cups) were causing visual clutter in screen reader outputs and are now hidden. Buttons that act as disabled need explicit ARIA hints (`aria-disabled="true"`) to convey their state beyond just the visual `opacity` lowering.

📸 Before/After:
No structural layout modifications. Emojis and states are now screen-reader friendly and follow established ARIA conventions for HTML templates.

♿ Accessibility:
- Increased compatibility with NVDA and VoiceOver.
- Screen readers now skip decorative elements instead of attempting to read raw Unicode character descriptions.
- Screen readers announce "Showing 1-50..." when the page is updated.
- Disabled navigation buttons properly announce their disabled state instead of leaving keyboard users confused.