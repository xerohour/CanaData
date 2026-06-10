## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-04-16 - Optimized recursive flattening logic
**Learning:** In highly recursive dictionary flattening, dynamically maintaining an iterative stack list of current path keys via `.pop()` and `append` combined with `.join()` operations causes significant O(n) overhead.
**Action:** Replace `keys.append(k)` and `.join(keys)` dynamically generated paths with a fixed paired stack tuple approach `(items, prefix)`.
