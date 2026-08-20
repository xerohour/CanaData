## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2024-06-30 - Optimized pandas column evaluation
**Learning:** Pandas `.where()` requires allocating an entirely new series mask for data manipulation and executes comparatively slow Python-level type checking loop internally, particularly when combined with `pd.to_numeric(errors="coerce")`.
**Action:** Replace `df[col] = numeric_col.where(numeric_col.notna(), original_col)` with `np.where(numeric_col.notna(), numeric_col, original_col)` which performs exactly the same operation using C-level array logic and without unnecessary series allocation overhead.
