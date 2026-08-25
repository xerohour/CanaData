## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-08-25 - [Optimize dictionary merges in parsing loop]
**Learning:** When appending or merging data into dictionaries within Python loops (such as during flattening), prefer direct loop key assignments (e.g., `for k, v in data.items(): result[k] = v`) over dictionary comprehensions passed to `.update()`. This avoids the overhead of allocating redundant intermediate dictionary objects.
**Action:** Replaced `.update({...})` calls that dynamically build dictionaries during large loop processing with direct key assignments to save memory and processing time.
