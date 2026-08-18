## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-06-31 - Dictionary merging vs updating and Pandas string conversions
**Learning:** Iterating using direct assignment (`for k, v in data.items(): result[k] = v`) avoids the overhead of intermediate object allocation caused by `.update()` when dictionaries are flattened. We previously observed that `to_numeric()` is a C-level vectorized operation, and although iterating `to_numpy()` with a try-except python fallback function may be microscopically faster in tests, introducing custom parser logic and breaking code readability violates the strict boundary "Never do: Sacrifice code readability for micro-optimizations". Re-aliasing standard python builtins to locals (e.g. `_dict = dict`) is also an anti-pattern.
**Action:** Avoid re-aliasing builtins. Use standard `.update()` logic when possible but if a micro-optimization is truly necessary, direct assignment in python loops can skip memory allocations. Preserve highly-optimized C-extensions like `pd.to_numeric` instead of re-implementing them.
