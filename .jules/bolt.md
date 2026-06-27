## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-27 - Pandas Memory Overhead and Object Iteration
**Learning:** Using `df[col].dropna()` creates significant memory overhead and can be very slow for N rows. Additionally, when using `.first_valid_index()`, if there are duplicate index labels, `.loc[first_idx]` returns a `pd.Series` rather than a scalar value. Finally, applying `.apply(lambda)` on pandas object columns is drastically slower than Python list comprehensions.
**Action:** Instead of `.dropna()`, use `if df[col].dtype == 'object'` and `first_idx = df[col].first_valid_index()`. Always check `isinstance(val, pd.Series)` and extract `.iloc[0]` if needed when accessing by `first_idx`. Use `[json.dumps(x) ... for x in df[col]]` instead of `.apply` for iterating through object columns.
