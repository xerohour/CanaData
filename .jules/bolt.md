## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-04-23 - [OptimizedDataProcessor Pandas Initialization Latency]
**Learning:** Utilizing Pandas DataFrames for small data transformations introduces substantial initialization latency (~35.5 ms mean time vs ~0.2 ms for native dictionaries).
**Action:** Future data processing pipelines must exclusively use batching techniques when utilizing heavy data analysis frameworks like pandas, reserving native primitive operations for continuous, low-latency item streams.
