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
## 2026-10-10 - Dictionary Unpacking Bottleneck
**Learning:** In Python 3.9+, when creating a new dictionary per item in a list comprehension (e.g., adding a location ID to menu items), using the dictionary union operator (`item | {"_location_id": location_id}`) is noticeably faster (~20%) than dictionary unpacking (`{**item, "_location_id": location_id}`) and avoids the overhead and readability loss of a manual `.append()` loop with `.copy()`.
**Action:** Use the dictionary union operator `|` within list comprehensions for performance-critical dictionary merging to maximize both speed and readability.
## 2026-10-10 - Optimize dictionary update with dict comp
**Learning:** Creating an intermediate dictionary with a comprehension just to immediately unpack it into another dictionary via `.update()` introduces unnecessary allocation overhead. Direct loop assignments are significantly faster.
**Action:** Replace `result.update({k: v for k, v in ...})` with `for k, v in ...: result[k] = v`.