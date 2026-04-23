## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-19 - Map-Reduce Aggregation for Shared State
**Learning:** Returning isolated map-reduce dictionaries from worker processes and merging them sequentially on the main thread is a highly scalable alternative to mutating global variables wrapped in locks (`threading.Lock()`).
**Action:** Always prefer map-reduce architectural patterns over shared mutable state when implementing multi-threaded batch processors.
