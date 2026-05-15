## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-16 - Stateless Worker Threads
**Learning:** Centralized thread locking during concurrent requests creates a "noisy neighbor" bottleneck preventing horizontal scale.
**Action:** Implemented stateless worker threads that return results individually for aggregation on the main thread, strictly avoiding thread locks on global mutable states.
