## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-04-16 - Pandas Data Processing Overhead
**Learning:** `.dropna()` creates a costly O(N) intermediate copy in Pandas, which is highly inefficient for merely finding the first valid item. Likewise, `.apply(lambda)` adds significant overhead per row for string conversion/JSON dumping on object columns.
**Action:** Use `df[col].first_valid_index()` for nested structure checking, and swap `df[col].apply(lambda)` for a list comprehension during JSON flattening on object columns.
