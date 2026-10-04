## 💡 What
Enhanced the accessibility of dynamically generated HTML in `CanaParse.py`.
- Added `aria-live="polite"` to the pagination status text ("Showing 1-10 of 50") so screen readers announce changes.
- Wrapped purely decorative sort icons (`↕`) with `aria-hidden="true"`.
- Added `aria-disabled="true"` and `cursor: not-allowed` to disabled pagination buttons.
- Handled emoji usage in the footer by properly wrapping ❤️ and ☕ with `role="img"` and descriptive `aria-label`s.

## 🎯 Why
These small UX and accessibility improvements make the interface significantly more usable for users relying on screen readers or keyboard navigation. By properly communicating live regions, disabled states, and meaningful vs decorative elements, the experience becomes much smoother.

## 📸 Before/After
N/A (Invisible semantic changes and minor CSS improvements on disabled buttons)

## ♿ Accessibility
- Fixed unannounced dynamic pagination text via `aria-live`
- Improved clarity of disabled controls for assistive tech
- Removed redundant noise from decorative emojis
- Provided meaningful alternatives for inline noun emojis
