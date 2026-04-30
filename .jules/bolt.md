## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-04-30 - O(N*M) Python list comprehension mutability and parsing overhead
**Learning:** In heavily executed loops (e.g., data filtering), dynamic string formatting operations (`" ".join(row)`) and uncompiled regex calls scale as O(N*M), creating a massive bottleneck. Additionally, filtering via list comprehension (`[row[:] for row in data if is_match(row)]`) is vulnerable to state leakage and slow execution when the `is_match` condition mutates the source elements before the defensive copy is made.
**Action:** Precalculate string representations and compile regex patterns at the class or module level to reduce O(N*M) overhead to O(N). Keep filter functions strictly pure and defer extracting derived values to rendering steps.
