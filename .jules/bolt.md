## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## $(date +%Y-%m-%d) - Pandas Object Column Iteration vs Apply
**Learning:** Using `.apply()` on pandas `object` columns has immense overhead compared to a basic Python list comprehension (`[f(x) for x in df[col]]`). Similarly, evaluating `dropna()` on entire columns just to find the first valid element is extremely slow; `first_valid_index()` is far more performant for type checking.
**Action:** Always favor list comprehensions over `.apply()` for simple element-wise transformations on pandas object columns, and use `first_valid_index()` rather than slicing operations to inspect data types.
