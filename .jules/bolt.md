## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-18 - Memory Cache O(n) Eviction
**Learning:** `_prune_memory_cache` was using an O(n) `min()` scan over standard `dict` keys to find the oldest entry, causing significant overhead as cache filled.
**Action:** Replace LRU logic in standard dictionaries with `collections.OrderedDict`, utilizing `move_to_end` and `popitem(last=False)` for O(1) time complexity.
