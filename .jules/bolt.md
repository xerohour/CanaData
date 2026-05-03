## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-05-03 - O(N*M) Formatting and Dynamic Regex Compilation in CanaParse
**Learning:** Dynamic string formatting (`" ".join(...)`) and `re.compile()` within the innermost O(N*M) filtering loop caused significant performance degradation. Additionally, mutating `row` state inside `is_match` (e.g. `row.append("thc+...")`) led to side effects across successive filters.
**Action:** Precompile regexes at the module level. Keep filter functions pure by removing `row.append` side effects. Use pre-calculated lowercased arrays for criteria and only compute the joined `row_str` when absolutely necessary for text-based filters to avoid massive overhead.
