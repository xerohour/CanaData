## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-02-18 - Defer state updates with Queues
**Learning:** Shared locks on mutable global arrays (`_menu_data_lock`) create "noisy neighbor" bottlenecks during high concurrency load, degrading throughput.
**Action:** Replace thread-locks with `queue.Queue()`. Defer dictionary updates to the queue in threads, then flush synchronously during final aggregation to resolve contention.
