# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Commands
- **Scraper**: `python3 CanaData.py` (interactive by default; use `-go <slug|mylist|all>` for quickrun)
- **Parser**: `python3 ./parse-script/CanaParse.py` (requires manual path config in script before run)
- **Install**: `pip3 install -r requirements.txt && pip3 install -r parse-script/requirements.txt`

## Architecture & Data Flow
- **CanaData.py**: Scrapes Weedmaps API. Outputs to `CanaData_MM-DD-YYYY/` directory.
- **CanaParse.py**: Processes CSVs from the scraper output. Path to CSV is hardcoded in `CanaParse.py` (`csv_folder` and `csv_file` variables).
- **Slug Management**: Slugs are read from `states.txt`, `slugs.txt`, and `mylist.txt`. `all` keyword uses `states.txt`.

## Non-Obvious Patterns
- **Directory Naming**: Scraper creates directories with current date `CanaData_%m-%d-%Y`. Parsers must be updated manually to match this date.
- **CSV Column Mapping**: `CanaParse.py` uses hardcoded column indices (e.g., `row[9]` for gram price). If Weedmaps API changes or `CanaData.py` flattens differently, indices will break.
- **Interactive Scraper**: Running `CanaData.py` without `-go` triggers input prompts for data types (dispensaries/deliveries).
- **Encoding**: Uses `utf-8` explicitly for CSV operations to handle special characters in product names.
