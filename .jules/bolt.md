## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-04-19 - Python Dictionary Normalization Overhead
**Learning:** In tight data normalization loops, using iterative `dict.copy()` and `.update()` degrades processing throughput significantly. Additionally, Python's `isinstance()` function incurs measurable latency compared to explicit `type(obj) is type` checks.
**Action:** Replace sequential dictionary updates with dictionary unpacking (`{**template_dict, **item}`) within list comprehensions. Substitute `isinstance` with `type(...) is` checks where polymorphism handles are not strictly necessary.
