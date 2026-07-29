## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2024-05-18 - Pandas List Comprehension Optimization
**Learning:** Iterating over `df[col]` directly or using `.apply()` with `isinstance` for object type checks is slower in pandas. Furthermore, `**kwargs` dictionary expansion in loops is slower than the Python 3.9 dict union operator `|`.
**Action:** Iterate over the underlying numpy array (`df[col].to_numpy()`) and strictly check types (`type(x) in (dict, list)`) with pre-bound local variables for maximum efficiency. Use `dict1 | dict2` in tight loops for faster dictionary merging.
