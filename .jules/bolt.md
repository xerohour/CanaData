## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-19 - Dictionary Flattening Overhead in OptimizedDataProcessor
**Learning:** Using `'.'.join(keys + [k])` for path construction inside deeply nested tight loops causes massive list allocation/concatenation overhead. Furthermore, multiple `isinstance` checks against custom types before falling back to primitive evaluation causes measurable latency per leaf node.
**Action:** Pre-compute key structures into a paired stack tuple `(items, prefix)` to eliminate dynamic array concatenations, and use explicit primitive type checking `isinstance(v, (str, int, float, bool))` as early fast-path returns when the upstream structure strictly guarantees leaf primitives (like parsed JSON).
