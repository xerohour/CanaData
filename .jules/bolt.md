## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-19 - Removed Thread Lock Bottleneck
**Learning:** Shared mutable state updated directly within worker threads necessitated `_menu_data_lock`, causing massive thread contention under high concurrency.
**Action:** Transitioned worker threads to be stateless. Worker functions now return parsed data dictionaries, which are collected concurrently and aggregated sequentially on the main thread, fully eliminating the global lock bottleneck.
