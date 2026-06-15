## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-06-15 - Removed Thread Bottleneck
**Learning:** Returning objects from threads and aggregating them in the main thread removes thread locking overhead completely.
**Action:** Always prefer stateless workers returning data to be aggregated synchronously.
