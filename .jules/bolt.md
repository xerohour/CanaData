## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-04-16 - Costly Nested Structure Detection
**Learning:** Using `df[col].dropna().head(10)` to probe columns for dictionaries or lists introduces severe O(N) allocation and copy overheads on large DataFrames.
**Action:** Future checks should use O(1) evaluation via `if df[col].dtype == 'object':` combined with `df[col].first_valid_index()` to inspect sample values without allocating copies.
