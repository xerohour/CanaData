## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-04-17 - Redundant String Casting in CanaData
**Learning:** The legacy `flatten_dictionary` method explicitly casted every leaf node to a string `str(v)`. Downstream, `optimized_data_processor` performs its own type normalization (e.g., to numeric or string representations), meaning `str(v)` caused a redundant allocation for each primitive node. Since we flatten extremely dense JSON documents containing numerous leaf nodes, this unneeded string conversion noticeably impacts overhead without any upstream benefit.
**Action:** Removed redundant `str(v)` cast directly in `flatten_dictionary` for leaf elements. In downstream `optimized_data_processor`, we still enforce `pandas` dtype logic, so correctness is unharmed and execution speed increases. Ensure methods that pass data downstream don't prematurely coerce variable types unless required.
