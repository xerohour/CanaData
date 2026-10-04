## 💡 What
- Added `aria-live="polite"` to dynamic status text updates (e.g., pagination info).
- Added `aria-disabled="true"` to buttons that are visually disabled with `cursor: not-allowed` and opacity changes.
- Wrapped purely decorative emojis in `<span aria-hidden="true">` to prevent screen readers from reading them aloud incorrectly.

## 🎯 Why
These changes enhance accessibility for screen reader users by ensuring dynamic UI updates are announced, disabled state semantics match their visual presentation, and purely decorative visual elements do not disrupt reading flow.

## 📸 Before/After
**Before:**
- Pagination showing "Showing 1-10 of 100" did not announce when updated.
- Disabled Previous/Next buttons only used visual cues (`opacity` and `disabled` property).
- Decorative emojis in empty states and footers were read aloud by screen readers.

**After:**
- Screen readers politely announce pagination updates.
- Screen readers accurately identify disabled buttons.
- Purely decorative emojis are ignored by screen readers, improving the reading experience.

## ♿ Accessibility
This PR strictly focuses on improving accessibility, particularly for users reliant on assistive technologies like screen readers, adhering to WAI-ARIA best practices.
