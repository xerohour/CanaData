## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## $(date +%Y-%m-%d) - [Pandas O(N) memory overhead with dropna]
**Learning:** Found that `df[col].dropna().head(10)` creates O(N) memory overhead for massive datasets when checking object columns. Also, `apply(lambda ...)` adds significant function overhead for type checking on object columns. Moreover, when using `first_valid_index()` with `loc[]`, duplicated indices can return a `pd.Series` rather than a scalar, which breaks simple `isinstance()` checks.
**Action:** Use `df[col].dtype == 'object'` combined with `first_valid_index()` for O(1) checks. Check for `pd.Series` on the `.loc[]` result if dealing with potentially duplicated indices. Use list comprehensions `[... for x in df[col]]` instead of `apply(lambda)` for much faster element-wise transformations on object columns.
