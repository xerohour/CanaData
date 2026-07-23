## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-23 - Python 3.9+ Dictionary Union Operator Performance
**Learning:** Iteratively building dictionaries in a loop using `template_dict.copy()` and `flat_ordered_dict.update(item)` is a significant performance bottleneck (0.87s per 10k iterations). Python 3.9's dictionary union operator (`|`) combined with list comprehensions (`[template | item for item in items]`) executes at C-speed, effectively reducing runtime by nearly 40% (0.54s per 10k).
**Action:** When creating uniform dictionaries or merging dicts in bulk data pipelines, always utilize the `|` operator and list comprehensions instead of iterative `.copy()` and `.update()` loops.
