## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-20 - Asynchronous State Aggregation
**Learning:** Centralized thread locking (`_menu_data_lock`) creates massive contention bottlenecks when horizontally scaling workers to append to global states (like `allMenuItems`).
**Action:** Implement a thread-safe `queue.Queue` to defer individual worker state updates, followed by an explicit `_aggregate_results()` batch execution step to synchronize states lock-free.
