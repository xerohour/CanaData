## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.

## 2026-07-02 - Removed global thread lock for better concurrency
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` dictionary prevented effective parallel execution and restricted the application to vertical scaling. Modifying the `CanaData` class processing methods to perform synchronous return of state variables over directly manipulating a locked global mutable array removed this bottleneck.
**Action:** Removed `_menu_data_lock` and refactored state aggregation logic, resulting in faster and lock-free execution suitable for high-load multithreaded systems. Future features requiring aggregated data should prefer returning payloads and centralizing the collection rather than acquiring locks on global shared properties.
