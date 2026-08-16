## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2024-08-16 - Evaluated Implicit Truthiness Optimization\n**Learning:** Using implicit truthiness checks (`if v:` or `if not item:`) in place of `len()` inside nested data structure parsing functions provides measurable function overhead reduction in CPython, especially for dictionary parsing loops.\n**Action:** Proactively replace `len(obj) > 0` and `len(obj.keys()) < 1` with truthiness evaluation in Python processing scripts to improve maintainability and micro-performance.
