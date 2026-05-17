## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-17 - Dictionary Flattening Optimization
**Learning:** In tight recursive or iterative loops simulating recursion (like dictionary flattening), function-call overhead from methods like `len()` or list methods can be a significant bottleneck. Using implicit boolean evaluations (`if v:`) and caching functions like `'.'.join` can yield substantial ~15% performance boosts. Furthermore, adding a fast path for primitive types at the start of loop processing avoids unnecessary type-checking logic for the most common case.
**Action:** Always evaluate tight loops for function-call overhead reduction and prioritize common fast-paths over complete type-checking cascades.
