## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-14 - Stateless concurrent parsing
**Learning:** The central state array with a thread lock became a major bottleneck during concurrent fetching.
**Action:** Moved the parsing to a stateless worker thread implementation that aggregates results back on the main thread, allowing for seamless horizontal scaling without lock contention.
