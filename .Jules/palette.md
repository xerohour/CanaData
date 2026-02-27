## 2026-02-27 - Glassmorphism Accessibility
**Learning:** Glassmorphism designs often suffer from poor focus visibility due to low-contrast backgrounds and transparent surfaces.
**Action:** Always pair `backdrop-filter` styles with explicit `:focus-visible` outlines using a high-contrast accent color (like `var(--secondary)` in this case) to ensure keyboard users can navigate safely. Also, ensure "Skip to content" links are present when large headers/hero sections exist.
