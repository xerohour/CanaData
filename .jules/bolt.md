## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.

## 2026-07-06 - Optimized dictionary flattening in CanaData
**Learning:** `flatten_dictionary` relies heavily on `isinstance()` checks and `len(v.keys())` when flattening thousands of menu items. Using explicit type equality checks (`type(v) is dict`) and implicit boolean evaluations (`if not v`) is significantly faster and saves substantial CPU time during massive processing loops.
**Action:** Use direct type checking and truthiness evaluation over `isinstance()` and explicit length checks when traversing deeply nested, high-volume data structures.
