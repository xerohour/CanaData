## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.
## 2026-05-18 - Tight Loop Overhead Anti-pattern
**Learning:** In tight iterative algorithms (like flattening millions of parsed JSON elements), standard Python readability conventions like `len(x.keys()) < 1` or `len(x) > 0` introduce massive function-call overhead that scales horribly, acting as a massive processing bottleneck compared to direct implicit evaluation `if not x:`.
**Action:** Use implicit boolean evaluation, pre-cache repetitively used built-in methods (like `join = '.'.join`), and use strict type checking (`type(x) is`) in critical fast-paths instead of relying on `isinstance` when exact object types are guaranteed.
