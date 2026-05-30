## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-30 - Optimize dict iteration and list concatenation for flattening algorithm
**Learning:** Python overheads like `dict.update()` with dictionary comprehensions or string interpolations inside a tight loop slow down heavily nested dict flattening. The `['.'.join(keys + [k])]` creates intermediate lists every iteration. Pushing `k` onto `keys`, using `'.'.join(keys)`, and popping `k` off is much faster. Also using direct type checks avoids the `isinstance` slowdown.
**Action:** Always favor pushing/popping to a shared stack/list over creating short-lived intermediate lists, and avoid intermediate dictionary allocations inside loop paths.
