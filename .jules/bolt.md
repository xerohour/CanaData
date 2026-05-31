## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-31 - Optimize string joins and length checks
**Learning:** In tight loops over deeply nested JSON representations, `len(v.keys()) < 1` or `len(v) > 0` and on-the-fly execution of `'.'.join(keys)` become significant bottlenecks. Implicit booleans (like `if v:` or `if not item:`) combined with assigning `join_keys = '.'.join` at the method's start avoids redundant allocations and function calls.
**Action:** Use fast implicit boolean evaluation (`if v:`) instead of `.keys()` counts to check dict lengths, and pre-cache frequently-called global functions inside performance-critical parsing functions.
