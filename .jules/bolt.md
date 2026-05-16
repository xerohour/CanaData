## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-24 - Stateless Concurrency Refactor
**Learning:** Thread locks on global mutable states (`_menu_data_lock`) cause severe bottlenecks ("noisy neighbor" issues) during high concurrency execution, capping multi-threading throughput regardless of hardware scaling.
**Action:** Instead of mutating global state directly inside worker functions, refactor worker functions to be stateless by returning parsed results. Then, iterate sequentially over the aggregated concurrent results array on the main thread to safely update the global dataset.
