## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-01 - Pandas Loop Bottlenecks
**Learning:** When dealing with heavy loop initializations and data processing in Pandas, iterating directly through Series and instantiating large lists using `{**item, ...}` is computationally expensive compared to accessing `.to_numpy()` and `.copy()`. Pre-computing strings like `.lower()` saves overhead.
**Action:** Use `.to_numpy()` with cached methods `_dumps` and explicit type checks in list comprehensions. Prefer `item.copy()` and `_append()` for constructing batched lists before Pandas ingestion.
