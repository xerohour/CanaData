## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-26 - Python Dictionary Evaluation Optimization
**Learning:** Checking dictionary emptiness via `len(x.keys()) < 1` incurs significant overhead in tight loops due to function calls and list instantiations, bottlenecking recursive processing.
**Action:** Always use implicit boolean evaluation (`if not x:`) and pre-cache repetitive built-in methods (e.g., `join_keys = '.'.join`) for critical path performance.
