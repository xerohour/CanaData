## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.

## 2026-08-07 - Optimized pandas normalization logic
**Learning:** Using `pd.to_numeric` followed by `.where` is slow. Iterating over the underlying numpy array (e.g., `df[col].to_numpy()`) using list comprehensions and explicit type conversion with try-catch is significantly faster than using vectorized pandas functions like `to_numeric` when handling highly mixed numeric/string columns.
**Action:** Prefer using list comprehensions with `to_numpy()` for complex value transformations on DataFrames over chaining multiple pandas operations.

## 2026-08-07 - Optimized dictionary flattening and grouping
**Learning:** Using explicit type assignments (`_dict = dict`) and boolean implicit checks inside the core flatten loop speeds up dict traversal. When organizing a list of dictionaries, avoiding `dict.copy()` + `dict.update()` in an inner loop by initializing a template dictionary and updating it directly, or avoiding `copy()` on a loop variable, significantly improves performance.
**Action:** Utilize implicit truthiness checking and avoid unnecessary intermediate dictionaries when flattening and merging large sets of JSON data.
