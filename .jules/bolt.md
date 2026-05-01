## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-05-01 - O(N*M) Overhead in CanaParse Filtering
**Learning:** The `is_match` function dynamically converts entire rows to strings inside a loop over every filter (M filters * N rows), leading to massive redundant string formatting overhead and slowing down applying filters.
**Action:** Precalculate row string representations once before iterating through filters and pass them down. Avoid mutating source data within filter conditions (e.g. `row.append`) to keep downstream iterations clean and memory leak free. Precompile regex patterns globally.
