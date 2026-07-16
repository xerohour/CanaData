## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-16 - Replaced pandas json_normalize with dictionary unpacking
**Learning:** Using pandas DataFrame and `pd.json_normalize` for dictionary flattening is highly inefficient in terms of memory overhead and object casting when compared to native python list comprehensions and dictionary unpacking. Pandas creates heavy copies when creating records.
**Action:** Replace pandas data parsing or normalization methods with pure python equivalents and `{**template, **item}` dictionary unpacking for performance.
