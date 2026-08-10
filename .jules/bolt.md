## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-08-10 - Padding Dictionary Loop Overhead
**Learning:** In CPython, `dict.copy()` and `dict.update()` execute entirely at the C level and are extraordinarily fast. Replacing them with a manual `for k in _all_keys:` loop forces the interpreter to evaluate all possible keys in Python-space for every single item, which will likely benchmark as slower than the original code despite avoiding a dictionary allocation.
**Action:** Do not attempt to optimize C-level dictionary merging or updating operations (like `.update()`) by replacing them with Python loops. Instead, look for algorithmic improvements or optimizations that can be pushed down to C level operations.
