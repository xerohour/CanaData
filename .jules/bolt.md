## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-01 - Replace Pandas with pure Python for JSON flattening
**Learning:** Pandas `json_normalize` and DataFrames introduce massive overhead for initialization, type inference, casting, and memory allocations, making them unsuited for quickly flattening wide JSON API payloads. Pure Python list comprehensions and dictionaries are often an order of magnitude faster for this task.
**Action:** When flattening and normalizing large, predictable JSON API payloads into dictionaries, prefer pure Python list comprehensions and dictionary unpacking over Pandas methods.
