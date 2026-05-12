## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-12 - ConcurrentMenuProcessor Rate Limiting Lock Contention
**Learning:** The thread lock inside `ConcurrentMenuProcessor._wait_for_rate_limit` covered the `time.sleep()` call. This forced worker threads to sleep sequentially rather than concurrently, drastically increasing the total execution time across threads and eliminating the benefit of parallel fetches.
**Action:** When implementing thread locks for tracking shared states like rate limit timers, always pre-calculate the sleep delta and execute the actual `time.sleep()` outside of the `with self.request_lock:` block to prevent cascading blocking delays.
