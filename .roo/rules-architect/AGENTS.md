# AGENTS.md (Architect Mode)

- The system follows a Scrape-then-Parse workflow with intermediate CSV storage.
- Coupling exists between `CanaData.py`'s flattening logic and `CanaParse.py`'s column indexing; changes to one require manual updates to the other.
- Data persistence is directory-based, versioned by date (`CanaData_MM-DD-YYYY`).
- Filtering logic is centralized in `parse-script/flower-filters.json` and applied during the parsing phase.
