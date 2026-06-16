## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-18 - Type Check and Method Caching Optimization
**Learning:** In highly recursive functions like nested dictionary flattening, MRO traversal overhead from `isinstance()` and function-call overhead from repeated `.join()` or `.append()` calls become significant performance bottlenecks. Exact type checks (`type(x) is dict`) and pre-caching built-in methods provide a measurable speedup.
**Action:** When writing or optimizing tight loops parsing massive data structures, pre-cache repetitively accessed bound methods and replace `isinstance` with exact `type()` checks when strict object types are guaranteed.
