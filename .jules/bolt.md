## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-28 - Artificial Benchmarking vs True Performance
**Learning:** Benchmarks utilizing artificial delays (e.g., `time.sleep()`) within global state locks fabricate non-existent scaling limitations. In CanaData, `_menu_data_lock` only synchronized O(1) dictionary assignments, meaning the global lock is not a bottleneck. Additionally, `pandas.json_normalize` and `.apply` incur massive overhead on unpredictable, nested JSON objects compared to pure Python dictionary list comprehensions.
**Action:** Always test the actual processing logic (e.g., `process_menu_json()`) rather than creating mock delays, and prefer native Python comprehensions/unpacking over Pandas DataFrame instantiations when flattening complex JSON payloads for high-performance extraction.
