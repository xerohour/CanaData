## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-19 - O(N) Dictionary & Pandas Operations Bottleneck
**Learning:** Using `isinstance()` with tuple classes inside tight loops for deeply nested dictionaries incurs significant MRO traversal overhead. Pandas `.apply(lambda)` for JSON serializations is dramatically slower than using standard Python list comprehensions.
**Action:** Replace `isinstance()` checks with explicit `type()` checking for exact JSON types, and replace `.apply(lambda)` row iterations with list comprehensions for text/JSON-based pandas object columns.
