## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-04-20 - Initialization Overhead in pandas DataFrames
**Learning:** Utilizing Pandas DataFrames for small data transformations introduces substantial initialization latency (~37.7 ms per instantiation) compared to raw Python primitives (~268 μs). This approach is highly inefficient for real-time or streaming single-item processing.
**Action:** Future data processing pipelines must exclusively use batching techniques when utilizing heavy data analysis frameworks like pandas, reserving native primitive operations for continuous, low-latency item streams.
