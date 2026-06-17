## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-18 - Dictionary Flattening Overhead
**Learning:** Frequent method lookups (e.g. `keys.append`) and `isinstance()` checks inside deeply nested tight loops parsing JSON payloads introduce significant O(N) allocation and MRO traversal overhead.
**Action:** Pre-cache instance methods and use exact type checks (`type(x) is dict`) to drastically reduce Python VM overhead in high-throughput parsing loops.
