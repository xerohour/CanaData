## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.

## 2026-07-18 - Replacing pandas with pure Python dict ops for normalization
**Learning:** Using pandas `json_normalize` and converting to DataFrame for flattening nested structures introduces huge overhead on small JSON chunks due to initialization, copying, and type inference.
**Action:** Replaced pandas logic entirely with pure Python nested dictionary processing and fast dictionary unpacking, which reduced execution times from 25ms to 0.5ms on benchmarks.
