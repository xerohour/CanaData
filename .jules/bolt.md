## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-04-16 - Lock Contention Mitigation in Python Multi-threading
**Learning:** Moving synchronization primitives out of parallel worker routines onto the main thread (synchronously aggregating returned outputs) completely removes thread blocking overhead and yields significant performance improvements over locking a shared dictionary.
**Action:** When mapping IO bound concurrent operations, pass the data state downward rather than mutating upward behind a global lock. Wait for futures to resolve and gather states sequentially.
