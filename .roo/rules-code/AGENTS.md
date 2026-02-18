# AGENTS.md (Code Mode)

- Always verify `csv_folder` and `csv_file` in `parse-script/CanaParse.py` before running, as they are hardcoded to specific dates/states.
- CSV column indices in `CanaParse.py` (e.g., `row[9]`, `row[20]`) are critical; verify them against `CanaData.py`'s `flatten_dictionary` output if the API structure changes.
- Use `encoding='utf-8'` for all file I/O to maintain compatibility with product names containing special characters.
- Scraper output is volatile; it creates a new directory daily based on `CanaData_%m-%d-%Y`.
