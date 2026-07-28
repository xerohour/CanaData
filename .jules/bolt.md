## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-06-30 - Optimized dictionary merging and set union in loop
**Learning:** Using `dict.copy()` and `dict.update()` inside a loop for dictionary padding is inefficient compared to Python 3.9's dictionary union operator `|`. Similarly, iterating through a list of dicts to update a set of keys one-by-one is slower than `set().union(*(d.keys() for d in dict_list))`.
**Action:** Use list comprehensions combined with `|` for dictionary padding, as it executes at C-speed and reduces latency significantly. Use `set().union()` with generators to avoid loop overhead when aggregating keys.
