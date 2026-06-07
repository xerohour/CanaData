## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-06-07 - Optimize pandas DataFrame column type inspection
**Learning:** Checking for nested list/dict types in pandas using `df[col].dropna().head(10)` creates a massive O(N) performance bottleneck because it allocates a new series and drops nulls across the entire column dataset just to inspect a single type.
**Action:** When inspecting pandas column contents for object types (like lists or dicts), always use `if df[col].dtype == 'object':` combined with `df[col].first_valid_index()` to achieve an O(1) type check without memory allocation overhead.
