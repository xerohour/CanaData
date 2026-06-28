## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-06-28 - Pandas Object Column Optimization
**Learning:** Using `df[col].dropna().head()` to check for nested data structures creates unnecessary memory overhead. Similarly, using `.apply(lambda)` for string formatting on pandas object columns is noticeably slower than standard list comprehensions due to Pandas' series iteration overhead.
**Action:** Always check `dtype == 'object'` and use `first_valid_index()` to safely extract a scalar representation for type-checking without overhead. Prefer list comprehensions `[format(x) for x in df[col]]` over `.apply(lambda)` when iterating over Pandas Object columns that require external functions.
