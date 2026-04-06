## 2026-02-24 - Static HTML Report Accessibility
**Learning:** The generated HTML report (`listing_report.html`) lacked basic keyboard accessibility features like focus indicators and skip links, making it difficult for keyboard-only users to navigate the large grid of listings.
**Action:** Added global `:focus-visible` styles and a `.skip-link` with inline CSS to `generate_report.py`. Ensure future generated reports include these styles by default.

## 2024-04-06 - Desktop GUI Keyboard Accessibility
**Learning:** Basic keyboard interactions are essential for desktop utility apps. Users expect forms to autofocus inputs and respond to the "Enter" key for submission, mimicking web form behavior. Lack of this creates friction for power users.
**Action:** Added `<Return>` key bindings to the root window to trigger form submission, and added `focus()` calls when enabling text entries in `scripts/gui_app.py`. Ensure future Tkinter/desktop UI scripts include these fundamental keyboard shortcuts.
