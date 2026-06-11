## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-06-11 - Stateless Worker Aggregation
**Learning:** Mutating global state within worker threads via locking creates severe lock contention under high concurrency.
**Action:** Refactored workers to be stateless by returning parsed dictionaries, shifting aggregation to a synchronous main-thread operation, thereby eliminating lock contention and enabling horizontal scalability.
