## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-05-17 - Pandas DataFrame Initialization Penalty
**Learning:** DataFrame instantiation via pandas incurs massive overhead (~32ms per batch) compared to iterative dictionary parsing (~200μs), making batch processors inefficient for small, continuous payloads.
**Action:** When designing data pipelines, ensure batch processors operate on large enough chunks to amortize initialization costs.
