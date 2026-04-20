## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-04-20 - Dictionary Unpacking Performance Gain
**Learning:** For dictionary mutations during iteration, dictionary unpacking (`{**template_dict, **item}`) inside a list comprehension is significantly faster (approx. 50% faster) than iteratively calling `.copy()` and `.update(item)` in a loop when handling large lists of uniform dictionaries.
**Action:** Prefer dictionary unpacking within list comprehensions over `.copy()` and `.update()` loops when creating large lists of uniform dictionaries from non-uniform data.
