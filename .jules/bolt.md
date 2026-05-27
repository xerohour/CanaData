## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-05-27 - Optimizing flatten_dictionary
**Learning:** In highly recursive or deep iteration paths like `flatten_dictionary`, repetitive function calls like `'.'.join(keys)` and expensive dictionary key length checks like `len(v.keys()) < 1` significantly slow down execution. Reordering conditional checks by frequency (putting `isinstance(v, dict)` first) optimizes hot paths. However, replacing `isinstance` with exact type checks (e.g., `type(x) is list`) should be avoided unless exact object types are strictly guaranteed, as this can cause structural robustness regressions with inherited or custom types.
**Action:** Pre-cache string methods (e.g., `join_keys = '.'.join`), replace O(n) checks with O(1) implicit boolean evaluation (`if not x:`), and order conditional `isinstance` checks to evaluate the most common structures first.
