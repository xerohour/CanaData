## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-05-16 - Fast Path Primitive Unrolling in Recursive Dictionaries
**Learning:** The legacy iterative stack flattening algorithm suffered huge penalties because `len()`, string `.join()` and condition matching inside a deep tight loop incurred huge function-call overhead.
**Action:** Pre-cache repetitive built-in methods, replace `len(x)` with implicit boolean checking, and fast-path primitive data early out of the loops, achieving roughly 20% speedup per dictionary iteration.
