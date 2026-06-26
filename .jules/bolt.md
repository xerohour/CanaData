## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-26 - Truthiness vs Materialized Views in Recursion
**Learning:** Checking `len(dict.keys())` incurs significant overhead in highly recursive/iterative functions because Python materializes a view of the keys before calculating the length (O(n)). Native truthiness checks (`if not dict:`) evaluate lazily (O(1)) and bypass this overhead.
**Action:** When profiling reveals high call counts to `{method 'keys' of 'dict' objects}` during dictionary processing or flattening, immediately refactor boolean checks to use implicit truthiness (`if obj:` or `if not obj:`) instead of `.keys()` length.
