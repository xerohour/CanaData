## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-18 - Dictionary Flattening Optimization
**Learning:** Flattening highly-nested dictionaries via iterative list concatenation (`keys + [k]`) and `'.'.join(keys)` has O(N) memory allocation and string concatenation overhead which slows down the processing loop significantly. Checking `isinstance(x, type)` is also slightly slower than exact type evaluation when subclasses are not expected.
**Action:** Used a paired stack tuple `(items, prefix)` to track paths incrementally (`f"{prefix}.{k}"`), yielding roughly 1.4-1.5x speedups in the recursive flattening step. Also substituted `type(x) is` for exact type checking.
