## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-24 - Pandas and List Comprehension Optimizations
**Learning:** List comprehensions with `**` dictionary unpacking are significantly faster than `.copy()` and `.append()` loops. Replacing O(N) memory allocation operations like `df[col].dropna()` with O(1) checks (`df[col].first_valid_index()`) combined with careful index handling (`loc` vs `iloc`, `pd.Series` deduplication) improves performance. Similarly, replacing `.apply(lambda)` on object columns with list comprehensions speeds up iteration in Pandas DataFrames.
**Action:** Always prefer list comprehensions over nested `.append()` and `.apply(lambda)` for Pandas object column operations. Avoid `.dropna()` for type-checking large dataframes.
