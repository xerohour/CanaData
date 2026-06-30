## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-30 - Pandas Apply vs List Comprehension on Object Columns
**Learning:** Using `.apply(lambda x: ...)` on pandas DataFrame object columns with Python types (like lists and dicts) has massive iteration overhead compared to Python list comprehensions. Furthermore, determining if a column contains nested structures via `df[col].dropna().head(10)` causes unnecessary copying and computation compared to inspecting the first valid index (`first_valid_index()`).
**Action:** When handling complex objects inside pandas DataFrames in the future, prefer standard Python list comprehensions (e.g., `[json.dumps(x) if ... else str(x) for x in df[col]]`) to drastically reduce Python-to-C API transitions and processing overhead.
