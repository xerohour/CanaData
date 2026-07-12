## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-12 - Replacing Pandas normalization with native Python
**Learning:** Flattening and normalizing large JSON payloads using `pd.json_normalize` and `df.to_dict('records')` introduces massive overhead due to type inference and DataFrame instantiation, becoming a bottleneck for large datasets.
**Action:** Use pure Python list comprehensions and dictionary unpacking with a pre-computed template (`{**template, **item}`) for flattening, and implement fast string checks (`isdigit()`) before coercing types to maintain performance.
