## 2024-05-22 - Path Traversal in File Export
**Vulnerability:** User input (`searchSlug`) was used directly in file path construction within `csv_maker`, allowing path traversal (e.g., `../../file.csv`) to write files outside the intended directory.
**Learning:** Even when file paths seem to be constructed with a safe base directory (`home_dir`), appending unsanitized user input can allow breaking out of that directory using `..`.
**Prevention:** Always sanitize user input used in file paths. Use `os.path.basename` to strip directory components and/or regex to whitelist allowed characters.
