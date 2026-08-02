## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-08-02 - Optimized pandas column mapping
**Learning:** Iterating over the underlying numpy array (e.g., `df[col].to_numpy()`) using list comprehensions and strict type checking (`type(x) in (dict, list)`) with pre-bound local variables is significantly faster than using pandas Series iteration or `isinstance`.
**Action:** Always prefer `.to_numpy()` and explicit `type()` checks in inner loops when transforming columns in large DataFrames to reduce overhead.
