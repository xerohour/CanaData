## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-18 - Pandas Object Column Flattening Optimization
**Learning:** Using `df[col].apply(lambda x: ...)` on pandas object columns is extremely slow due to pandas' internal loop overhead. Replacing it with standard python list comprehensions (e.g., `[json.dumps(x) ... for x in df[col]]`) significantly speeds up data manipulation overhead. Additionally, to check if a column contains nested objects, checking `first_valid_index()` is much faster than `df[col].dropna()`.
**Action:** Always prefer list comprehensions over `.apply()` for element-wise string transformations on pandas object columns to maximize throughput.
