## 2026-02-26 - Navigation Accessibility in Grid Layouts
**Learning:** In data-heavy grid layouts like the discovery report, keyboard users are forced to tab through potentially hundreds of cards and their internal links. Without a skip link, the experience is tedious and practically unusable for keyboard-only users.
**Action:** Always implement a "Skip to Main Content" link as the first focusable element on generated reports, and ensure all external links opening in new tabs have `rel="noopener noreferrer"` and descriptive `aria-label`s to announce the behavior.
