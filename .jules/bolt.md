## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-04-16 - Pandas Data Processing Optimizations
**Learning:** List comprehensions on Pandas object columns are significantly faster than `.apply(lambda)`. Using `first_valid_index()` is memory-efficient for type checking.
**Action:** Use these techniques for large batch operations on unstructured data.
