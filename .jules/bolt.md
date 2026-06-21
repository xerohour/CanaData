## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-21 - Python List Comprehension vs Pandas Apply
**Learning:** When optimizing Pandas operations on object columns (e.g., string formatting or type conversions), applying a native Python list comprehension executes significantly faster than using `.apply(lambda)` due to reduced Pandas series overhead.
**Action:** Default to list comprehensions for object column string operations in pandas dataframes to maximize batch processing throughput.
