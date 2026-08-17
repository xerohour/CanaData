## Performance Learnings

## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.

## 2026-08-17 - Delaying text concatenation in large datasets
**Learning:** When performing text-based search filters against multiple string columns, eagerly joining the row array `row_str = " ".join([str(x) for x in row]).lower()` incurs high string allocation and memory overhead, even if preceding exact-match criteria (like Categories or Brands) fail.
**Action:** Delay joining row strings until explicitly needed by text-based filters. Use generator expressions `map(str, row)` instead of list comprehensions when joining to avoid intermediate array allocation. Restructure conditional checks to evaluate O(1) dictionary lookups or exact matches before triggering O(N) string transformations.
