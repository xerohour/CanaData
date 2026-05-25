## 2025-05-25 - Skip Link and Alt Text Improvements
**Learning:** Skip links need the target container to have `tabindex="-1"` so it can programmatically receive focus, otherwise standard elements like `<div>` will not shift focus correctly. Also, duplicate screen reader announcements happen if an image `alt` text matches the text of the immediately following heading.
**Action:** Always add `tabindex="-1"` to the target of a skip link. Use empty `alt=""` attributes for images when the exact text is presented adjacently to avoid screen reader noise.
