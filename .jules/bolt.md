## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-06-18 - Pandas processing optimization in CanaData
**Learning:** Using `pandas` `.apply(lambda)`, iterating over columns dynamically doing string comparisons, and calling `.dropna().head(10)` are surprisingly slow for large DataFrames.
**Action:** Replaced `.apply(lambda)` with list comprehensions which run significantly faster over object columns. Avoided `.dropna().head(10)` for nested value checks by checking `df[col].dtype == 'object'` and `df[col].first_valid_index()`. Avoided looping all columns by filtering column names once up-front. Avoided `dict.copy()` by using `dict(item, _location_id=...)` in a list comprehension.
