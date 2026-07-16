## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-06-28 - Artificial Delays in Concurrency Testing
**Learning:** Adding `time.sleep()` to benchmark global lock contention falsifies real-world latency by over-representing context switching delays, leading to inaccurate architectural conclusions about 'severe lock contention' which in reality was just an O(1) dictionary assignment.
**Action:** Always profile the codebase's actual real logic and methods natively without artificial delays to accurately audit application performance and scalability bottlenecks.

## 2026-06-28 - Pandas Overhead on JSON Normalization
**Learning:** `pandas.json_normalize()` introduces severe overhead during wide DataFrame initialization and type inference for predictable JSON API payloads compared to native Python implementations.
**Action:** Prefer pure Python list comprehensions and dictionary unpacking `{**template, **item}` to normalize and flatten predictable JSON payloads to avoid Pandas instantiation and casting overhead.
