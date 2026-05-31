## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-01 - Resolved Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list creates a "noisy neighbor" bottleneck, hindering horizontal scaling under heavy multithreaded loads. Replacing the lock with a thread-safe message queue (`queue.Queue`) allows workers to deposit data asynchronously without blocking, shifting state aggregation to a final, deferred flush sequence.
**Action:** Default to queue-based state updates rather than centralized mutexes for parallel ingestion, ensuring `flush_queue()` is invoked sequentially before final structured outputs.
