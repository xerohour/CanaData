## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-21 - Thread Locking Replaced with Queue
**Learning:** Replaced `_menu_data_lock` with `queue.Queue` for thread-safe state aggregation, improving horizontal scalability.
**Action:** When gathering high volume data from parallel threads, enqueue results instead of sharing mutable arrays under locks to prevent noisy neighbor latency blockades.
