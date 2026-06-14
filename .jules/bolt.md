## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-14 - Optimize Hot Loop Type Checking
**Learning:** Inside deeply nested recursive-like loops (e.g., dictionary flattening), repeatedly calling `isinstance()` introduces massive overhead traversing MRO (Method Resolution Order). Checking `type(v) is dict` directly reduces execution time considerably when types are strict and known. Pre-caching built-ins (`type_fn = type`, etc) shaves off even more instruction cycles per iteration.
**Action:** Avoid `isinstance` for tight performance-sensitive loops if strict types are guaranteed.
