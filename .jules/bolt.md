## 2026-02-23 - Pandas vs Native Python Flattening
**Learning:** For small to medium datasets (e.g., 4000 items), pure Python dictionary flattening combined with `csv.DictWriter` is ~3x faster (0.06s vs 0.18s) than using `pandas.json_normalize` and `to_dict`. Pandas overhead dominates for simple JSON structures.
**Action:** Before reaching for Pandas for simple data transformation tasks, benchmark a native Python implementation, especially if dependencies are a concern.
