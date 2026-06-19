## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-19 - Removed thread lock to fix "noisy neighbor" scaling bottleneck
**Learning:** Legacy concurrent scrapers often use global shared state arrays protected by a `threading.Lock()` (like `_menu_data_lock` in `CanaData.py`). Under high concurrent workloads, worker threads spend the vast majority of their CPU time waiting for lock acquisition rather than performing computations, completely eliminating the benefit of parallel execution and causing a "noisy neighbor" scaling bottleneck.
**Action:** When horizontal scaling is required, migrate from global locked arrays to a functional map-reduce or stateless worker pattern where threads return their results individually (`executor.submit(func)` returning a payload), and the main thread synchronously aggregates them (e.g., `_aggregate_menu_result`) safely without locks. Ensure all non-code deliverables like audit plans or reports are implemented when requested.
