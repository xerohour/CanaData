💡 What: Improved accessibility of the inline emojis ("❤️" and "☕") in the generated HTML footer by wrapping them in `<span>` tags with `role="img"` and appropriate `aria-label`s.

🎯 Why: Screen readers often struggle to interpret raw unicode emojis, especially when they replace nouns in a sentence. This change preserves the grammatical flow of the sentence for screen reader users by supplying semantic meaning ("love" and "coffee") without hiding them.

📸 Before/After:
Before: `© 2026 CanaData Analytics • Generated with ❤️ and ☕`
After: `© 2026 CanaData Analytics • Generated with <span aria-label="love" role="img">❤️</span> and <span aria-label="coffee" role="img">☕</span>`

♿ Accessibility: Ensures that visually impaired users utilizing assistive technologies can properly understand the context of the generated footer.