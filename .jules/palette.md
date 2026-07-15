## 2026-07-15 - Skip to Main Content Focus Management
**Learning:** The 'skip to main content' accessibility link fails to actually move keyboard focus to the target container unless the target explicitly has `tabindex="-1"`.
**Action:** Added `tabindex="-1"` to the `#main-content` container in `generate_report.py` to ensure it programmatically receives focus when the skip link is activated.
