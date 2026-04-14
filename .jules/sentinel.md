## 2026-02-24 - Path Traversal in CSV Export
**Vulnerability:** User-controlled filenames in `csv_maker` allowed writing files outside the intended directory via `../` sequences.
**Learning:** Even internal utility functions like `csv_maker` can be vulnerable if they accept unsanitized input derived from user arguments (`searchSlug`).
**Prevention:** Always sanitize filenames using allowlists (alphanumeric, etc.) before using them in file operations, especially when they originate from user input.

## 2024-03-22 - XSS in HTML Report Generation
**Vulnerability:** User-controlled API responses (e.g., dispensary names, types, addresses, and URLs) were directly injected into raw f-strings in `generate_report.py` to create HTML reports.
**Learning:** Raw f-strings do not inherently sanitize input. When injecting dynamic, external data into an HTML context, escaping must be done manually to prevent XSS. We also must ensure URL protocols are strictly whitelisted before escaping.
**Prevention:** Always wrap dynamically injected values with `html.escape(str(val))` when building raw HTML templates in Python. Also validate `.get()` defaults correctly when an explicit `None` might bypass them (e.g., using `val = item.get('key') or 'default'`).
