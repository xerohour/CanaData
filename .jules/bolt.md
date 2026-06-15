## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-15 - Dictionary Flattening Bottleneck Optimization
**Learning:** During extensive iterative dictionary flattening, `isinstance()` checks and dynamic loop-level list allocations (`'.'.join(keys)`, `keys.append(k)`, `len(x.keys()) < 1`) introduced major overhead (up to ~30-50% slower). Because the exact data types expected are static/strict primitives in our JSON schema, `isinstance` MRO resolution overhead can be bypassed safely. Checking dictionaries before lists in conditionals also yields quicker evaluations since dictionaries are far more frequent.
**Action:** Always pre-cache heavily utilized built-in methods (like `join_keys = '.'.join`), replace costly list allocation checks like `len(x.keys()) < 1` with O(1) implicit boolean checks (`not x`), and utilize direct `type(x) is` equality checks rather than `isinstance()` during recursive or tight-loop traversals.
