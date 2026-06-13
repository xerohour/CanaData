## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2025-06-13 - O(1) Prefix Stack over Array Mutations in CanaData
**Learning:** During highly nested JSON unrolling (`flatten_dictionary`), repeatedly performing list `.pop()`, `.append()`, and `.join()` per iteration becomes a critical CPU bottleneck. `type(v)` over `isinstance()` checks save MRO lookup overheads as well.
**Action:** Use a stack containing paired tuple values `[(iter(), prefix_string)]` to avoid array mutations entirely during recursion unrolling. Use exact object typing (`is dict`) when processing strictly defined JSON structures.
