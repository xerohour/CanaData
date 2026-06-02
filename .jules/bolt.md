## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2024-06-03 - Concurrency Thread Queue and Recursion Optimization
**Learning:** Legacy synchronous thread locking (`with self._menu_data_lock:`) forced worker threads to await lock acquisition before merging local dictionaries into the global state, causing a substantial "noisy neighbor" bottleneck and severely capping concurrent throughput. Furthermore, repetitive string operations within heavily recursive functions (`flatten_dictionary`) incurred high function-call overhead.
**Action:** Replaced thread locking with thread-safe `queue.Queue()`, allowing worker threads to immediately push payloads and return, while the main thread sequentially consumes the queue after executor completion. Additionally, cached repetitive string concatenations and replaced slow O(n) length evaluations (`len(x.keys()) < 1`) with O(1) truthiness checks (`not x`) in hot recursive paths.
