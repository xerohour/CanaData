## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-04-16 - Flattening Tight Loop Optimization
**Learning:** `len(v.keys()) < 1` evaluates all keys using O(N) allocation before computing length, and `isinstance()` checks create considerable overhead when executed millions of times per recursive branch.
**Action:** In highly recursive inner loops, use exact primitive type checking (`type(x) is str`) first as a fast-path filter, and employ implicit boolean evaluations (`if not x:`) which are vastly faster in Python than calculating string/dictionary/list lengths. Pre-cache methods outside the loop to eliminate dictionary lookups.
