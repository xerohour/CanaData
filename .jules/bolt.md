## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-22 - Dictionary Merging Optimization
**Learning:** Using iterative `dict.copy()` and `dict.update()` inside heavy parsing loops incurs high Python-level overhead and negatively impacts processing latency.
**Action:** Use Python 3.9+ dictionary union operator (`|`) combined with list comprehensions (e.g., `[template | item for item in list]`) to execute dictionary merging at C-speed, avoiding manual iteration and allocation overhead.
