# AGENTS.md (Ask Mode)

- `CanaData.py` is the main scraper targeting Weedmaps Discovery API.
- `parse-script/CanaParse.py` is the data processor and HTML generator.
- Slugs are managed via `.txt` files in the root: `states.txt` (all states), `slugs.txt` (custom slugs), `mylist.txt` (user defined).
- The project uses `yattag` for HTML generation and standard Python libraries for CSV/JSON handling.
