## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-23 - Pandas Object Column Flattening Bottleneck
**Learning:** Checking DataFrame object columns for nested types using `df[col].dropna().head(10)` causes an O(N) memory allocation and processing overhead, scaling linearly with data size. Additionally, applying lambda functions (e.g., `.apply(lambda)`) to format strings is drastically slower than using a native Python list comprehension because pandas incurs significant overhead executing Python functions row-by-row on Series objects.
**Action:** When inspecting or formatting pandas object columns, use `df[col].first_valid_index()` to get O(1) type resolution (being mindful that duplicate indices can return a Series), and always use list comprehensions (`[fn(x) for x in df[col]]`) instead of `.apply()` for simple element-wise transformations on object/string columns.
