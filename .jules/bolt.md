## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-19 - Concurrent Result Queue Implementation
**Learning:** Returning objects into a `queue.Queue` within worker threads and systematically flushing that queue on the main thread via an aggregation method completely eradicates synchronization lock bottlenecks, solving the "noisy neighbor" issue. Furthermore, synchronous testing frameworks evaluating these batched results must be explicitly updated to invoke the aggregation method after joining executor threads but prior to assertion validation.
**Action:** Always favor asynchronous queues (`queue.Queue`) over global state locks (`threading.Lock`) for accumulating massive datasets in high-concurrency environments, and strictly ensure that tests manually aggregate state before validation.
