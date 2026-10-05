💡 What:
- Added `aria-live="polite"` to the pagination text and `aria-disabled="true"` with `cursor: not-allowed` to the disabled buttons in `parse-script/CanaParse.py`.
- Wrapped the decorative `✨` emoji in `generate_report.py` in `<span aria-hidden="true">`.
- Wrapped the inline noun emojis (`❤️` and `☕`) in the footer of `parse-script/CanaParse.py` in `<span role="img" aria-label="...">`.

🎯 Why:
- Screen readers do not announce dynamic pagination text changes without `aria-live`.
- A button disabled solely through JavaScript without the native HTML disabled attribute or `aria-disabled` may not be conveyed to screen readers. Adding `cursor: not-allowed` alongside these visual cues provide standard fallbacks.
- Decorative emojis are read out loudly by screen readers, disrupting the content flow.
- Inline noun emojis that act as parts of a sentence must be wrapped with a valid label so screen readers read the correct word instead of skipping or confusing the context.

📸 Before/After:
- No visual changes except cursor style when hovering over disabled pagination buttons.

♿ Accessibility:
- Vastly improved keyboard navigation and screen reader support for the pagination component.
- Enhanced context and natural reading flow for screen reader users by properly tagging informative and decorative emojis.