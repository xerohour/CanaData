## 2026-10-04 - Accessibility improvements for dynamic elements and emojis
**Learning:** Dynamic status text needs aria-live='polite', disabled buttons need aria-disabled='true', and purely decorative emojis need aria-hidden='true' to be fully accessible for screen readers.
**Action:** Added proper aria attributes to HTML strings in CanaParse.py and generate_report.py.
