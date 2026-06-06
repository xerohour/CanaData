## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-06 - Optimized flattening with tuple stacks
**Learning:** `flatten_dictionary` in Python is significantly faster without `iter()` and generator chaining `next()`, especially when prefix construction `'.'.join(keys)` can be fully circumvented using `stack = [(d.items(), prefix)]` and `pop`/`append` method caching. O(N) length checks like `len(dict.keys())` are also slow bottlenecks compared to implicit boolean evaluations `if not dict:`.
**Action:** Always favor implicit python truthy boolean checks over length calculations, and pass state along the stack instead of recalculating strings recursively where possible.
