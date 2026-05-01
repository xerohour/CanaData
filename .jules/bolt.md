## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-05-01 - Refactored State Aggregation to Lock-Free Map-Reduce
**Learning:** Using a global lock for thread synchronization creates a "noisy neighbor" vulnerability that restricts the application to vertical scaling only, making it unsuitable for distributed node execution.
**Action:** Refactor data ingestion pipelines to use a lock-free map-reduce model where stateless worker nodes return dictionaries of results, which are then sequentially merged by a central coordinator.
