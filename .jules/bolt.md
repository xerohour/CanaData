## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-25 - Pandas Object Column List Comprehension Optimization
**Learning:** In Pandas, iterating over object columns and using `apply(lambda ...)` for JSON conversion or type checks is significantly slower than applying a Python list comprehension directly to the column Series (e.g., `df[col] = [json.dumps(x) ... for x in df[col]]`). Additionally, O(N) column sampling for nested structs via `dropna().head(10)` can be eliminated entirely using O(1) checks on `first_valid_index()`.
**Action:** When normalizing Pandas object columns, particularly in wide dataframes, prefer list comprehensions over `apply(lambda)`, and utilize O(1) type inference indexing rather than allocating temporary slices.
