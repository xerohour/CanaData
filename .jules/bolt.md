## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-22 - Resolving Concurrency Bottleneck in CanaData
**Learning:** Thread locking over global shared state during high-frequency parallel write operations induces significant lock contention, which degrades throughput in a concurrent worker pool.
**Action:** Always implement a message-passing or queue-based aggregation pattern to defer state updates to a single synchronous execution phase, eliminating the need for locks in threaded operations.
