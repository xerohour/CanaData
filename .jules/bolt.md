## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2024-07-14 - Replace Pandas with Pure Python for JSON flattening
**Learning:** Using `pandas.json_normalize` and `DataFrame` for flattening and normalizing large nested JSON structures introduces massive overhead due to type inference and dataframe instantiation.
**Action:** Prefer pure Python list comprehensions and generator/stack-based patterns for flattening dictionaries, handling type coercion carefully.
