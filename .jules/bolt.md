## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-03 - Replaced O(n) .keys() length checks in hot loops
**Learning:** Replacing O(n) .keys() checks (e.g. len(item.keys()) < 1) with O(1) implicitly boolean evaluation (e.g. if not item:) in the hot loop drastically speeds up dictionary processing overhead without breaking dict subclass support.
**Action:** Check for and replace expensive dictionary/list length evaluations with implicit boolean comparisons inside recursive functions or iterative nested processors.
