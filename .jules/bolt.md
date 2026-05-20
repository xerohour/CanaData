## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-18 - Replacing Thread Locks with Asynchronous Queues
**Learning:** Centralized thread locking (`_menu_data_lock`) over the global `self.allMenuItems` dictionary limits concurrency. Writing updates to a `queue.Queue` during the scrape and aggregating them linearly after the fact prevents noisy-neighbor wait times and enables full horizontal scaling.
**Action:** Use lock-free data structures (like queues) or batched reductions to prevent centralized state mutation bottlenecks in multi-threaded flows.
