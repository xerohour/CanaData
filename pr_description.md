💡 What
Added accessibility features to the dynamically generated dashboard in `parse-script/CanaParse.py`. Specifically:
- Added `aria-live="polite"` to the dynamic pagination status text so screen readers announce changes.
- Added `aria-disabled="true"` to pagination buttons when they are visually disabled (`cursor: not-allowed` and `opacity: 0.5`).
- Added `aria-hidden="true"` to decorative table sort icons to reduce screen reader noise.
- Made the noun emojis in the footer (❤️ and ☕) accessible by wrapping them in `<span role="img">` with an `aria-label`.

🎯 Why
Users relying on assistive technologies need to be informed when data changes (e.g. changing pages), know the state of interactive elements, and hear content like emojis described accurately instead of just read out generically or skipped. These micro-improvements create a much more robust experience for screen reader users when interacting with the dynamic generated tables.

📸 Before/After
*(Visuals remain unchanged, but assistive tech will now correctly read the elements)*

♿ Accessibility
- Improves screen reader announcement of dynamic pagination changes.
- Reduces clutter by hiding purely visual sorting icons.
- Improves context for visually disabled navigation buttons.
- Makes footer emojis accessible text.