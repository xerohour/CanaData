## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-06-24 - [Optimize Pandas flattening]
**Learning:** Checking Pandas DataFrame columns for nested structures using `df[col].dropna()` introduces O(N) memory overhead. Using `first_valid_index()` is much faster, but you must check `.loc[first_idx]` and handle duplicate indices returning a `pd.Series`. Also, applying list comprehensions to Pandas object columns is significantly faster than using `.apply(lambda)`.
**Action:** Use `first_valid_index` and list comprehensions when processing or flattening object columns in Pandas.
