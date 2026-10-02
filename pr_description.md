💡 What:
Improved accessibility on pagination controls and decorative promo emoji.

🎯 Why:
To make the interface more inclusive for users navigating with assistive technology like screen readers, providing feedback on pagination changes and disabled button states, and avoiding confusing screen reader readout for purely visual emojis.

📸 Before/After:
Before: Disabled pagination buttons lacked ARIA attributes, status text didn't update screen readers, and promo block emoji was read out loud.
After: Disabled buttons use `aria-disabled="true"` and `cursor: not-allowed`. Status text uses `aria-live="polite"`. Purely decorative sparkle emoji uses `<span aria-hidden="true">`.

♿ Accessibility:
- Added `aria-live="polite"` to the dynamic pagination status text so screen readers announce "Showing X-Y of Z" updates.
- Added `aria-disabled="true"` and `cursor: not-allowed` to disabled pagination buttons.
- Added `<span aria-hidden="true">` to purely decorative sparkle emoji (✨) in promo sections.