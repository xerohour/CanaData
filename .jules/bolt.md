## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-05-30 - Optimize thread synchronization in CanaData
**Learning:** Global locking (`_menu_data_lock`) restricted concurrent extraction throughput. By removing the lock and deferring state aggregation using a thread-safe append to a main queue (`_menu_queue`), context switching and lock contention overheads were dramatically reduced.
**Action:** When gathering high volumes of fragmented API data across multiple threads, queue the raw results locally and append them to a central lock-free structure (like `list.append` in Python due to the GIL), then aggregate them fully in the main thread once extraction completes.
