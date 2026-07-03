## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-03 - Bypassing pandas for dict flattening
**Learning:** Using `pd.json_normalize` and `df.to_dict('records')` introduces massive overhead (taking ~6 seconds for 25k records vs ~1.6 seconds natively) due to Pandas type inference, casting, and dataframe instantiation.
**Action:** Always prefer native python list comprehensions, dictionary merging (`{**dict1, **dict2}`), and set unions for flattening and normalizing simple, predictable JSON API payloads.
