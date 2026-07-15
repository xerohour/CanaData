## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-06-30 - Optimized pandas column evaluation
**Learning:** Using `df[col].dropna()` in pandas has O(N) memory overhead and is slow for large DataFrames.
**Action:** Use `df[col].first_valid_index()` along with checking for duplicate indices to securely extract the first scalar value without allocating a full Series copy. Use list comprehensions over `.apply` for complex row operations.
## 2026-07-15 - Global Lock Concurrency Misdiagnosis
**Learning:** The previous benchmark incorrectly identified the _menu_data_lock as a concurrency bottleneck by mocking processing time with time.sleep(). When benchmarking actual logic, the lock only wraps O(1) in-memory assignments, meaning it does not hinder elastic scaling.
**Action:** Always benchmark real logic rather than using artificial delays, and avoid refactoring state architecture (like removing global locks) if they only protect fast memory writes.
