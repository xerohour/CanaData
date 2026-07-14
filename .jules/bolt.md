## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.

## 2026-07-14 - Artificial Bottlenecks in Stress Testing
**Learning:** Performance benchmarking using mock artificial delays (like `time.sleep()`) inside critical sections creates false contention metrics that do not reflect the application's actual logic execution time or real-world lock overhead.
**Action:** When implementing stress tests, always benchmark the actual payload manipulation logic and genuine method implementations to acquire accurate profiling insights.
