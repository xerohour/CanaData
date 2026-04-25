## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-18 - Dictionary Comprehension Loop Overhead
**Learning:** Building a large list of uniform dictionaries using a `for` loop with `.copy()` and `.update()` introduces significant overhead due to repeated method resolution and Python bytecode execution.
**Action:** When normalizing dictionaries to a uniform schema, prefer using dictionary unpacking inside a list comprehension (`[{**template_dict, **item} for item in items]`) to leverage CPython's fast internal list building and unpacking implementations.
