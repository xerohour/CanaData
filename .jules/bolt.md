## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-24 - Remove Centralized Thread Lock
**Learning:** Centralized thread locking (`_menu_data_lock`) over global state in `CanaData` restricts the application to vertical scaling and acts as a "noisy neighbor" bottleneck under high volume.
**Action:** Migrated to a stateless worker nodes architecture. Methods now return data dictionaries which are aggregated sequentially by the main thread, allowing `ConcurrentMenuProcessor` to efficiently run purely stateless background tasks without blocking.
