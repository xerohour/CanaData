## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-08-22 - Python Dictionary Unpacking Optimization
**Learning:** During large batch flattening transformations on lists of dictionaries, manual looping with `template.copy()` and `dict.update()` introduces O(N) allocation overhead.
**Action:** Use list comprehensions with modern dictionary unpacking `[{**template, **item} for item in items]` and `set().union(*(d.keys() for d in flatDictList))` to push loop overhead into optimized C execution paths.
