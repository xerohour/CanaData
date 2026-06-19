## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-06-19 - Micro-optimizations for Deep JSON structures
**Learning:** When flattening large deeply nested JSON objects, function call overhead inside the "while stack" iteration logic creates bottlenecks. Pre-caching builtins like .join and .append, using implicit boolean evaluation over len(x)>0, and using `type() is` rather than `isinstance()` reduces traversal cost.
**Action:** Use pre-cached builtins inside O(N) loops during recursive traversal structures on massive data sets.
