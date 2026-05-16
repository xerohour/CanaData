## 2024-05-16 - Accessible Rating Badges
**Learning:** Compact rating badges (e.g., '★ 4.5 (100)') are poorly interpreted by screen readers, which read the literal punctuation ('star four point five left paren...') instead of the intended meaning.
**Action:** Use an outer container with a descriptive `aria-label` (and `title` for mouse hover) and wrap the visual rating content in `aria-hidden="true"` to ensure clear, natural announcements without visual clutter.
