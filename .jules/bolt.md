## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-24 - Optimization: O(1) checks and caching string joins in loop
**Learning:** Python function calls inside tight loops (like `'.'.join()`) and calculating lengths of collections for conditional checks (`len(v) > 0`, `len(item.keys()) < 1`) introduce measurable overhead when recursively processing deeply nested JSON.
**Action:** Replaced O(N) length checks with O(1) implicit boolean evaluation (`if v:`, `if not item:`) and cached repetitive built-in methods (`join_keys = '.'.join`) outside the loop to eliminate function overhead.
