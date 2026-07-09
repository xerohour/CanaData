## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2024-05-15 - Pandas Normalization Overhead
**Learning:** Using `pandas.json_normalize()` and `df.to_dict('records')` for large JSON API payloads introduces massive overhead due to type inference, casting, and DataFrame instantiation compared to simple dictionary unpacking.
**Action:** When flattening predictable nested JSON structures into flat dictionaries (e.g. for CSV export), rely on pure Python list comprehensions and dictionary template unpacking (`{**template, **item}`) instead of instantiating Pandas DataFrames.
