## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2024-07-13 - Pure Python JSON Normalization
**Learning:** Flattening and normalizing large, predictable JSON API payloads into dictionaries or CSV-ready structures scales poorly in Pandas (like `pd.json_normalize` and `df.to_dict`) due to massive overhead of type inference, casting, and internal DataFrame instantiations.
**Action:** Prefer pure Python list comprehensions and iterative stack traversals over Pandas methods to significantly reduce execution overhead and improve performance. Implement generic type coercion using `try/except int/float` instead of hardcoding numeric keys, BUT be careful to constrain it to expected fields to avoid corrupting string IDs, zipcodes, etc.
