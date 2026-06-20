## Performance Learnings

## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2026-04-16 - Algorithmic Profiling and Flattening
**Learning:** The pandas-based batch `OptimizedDataProcessor` carries tremendous initialization overhead (~73,000 function calls) making it extremely slow for single/small JSON payloads compared to iterative stack flattening. Additionally, algorithm optimizations like replacing `len(x.keys()) < 1` with `if not x:` provide O(1) performance without sacrificing Python polymorphism or resorting to brittle micro-optimizations (like localizing built-ins or exact `type()` matching).
**Action:** When auditing performance, prioritize native profilers (like `cProfile`) to analyze internal call volumes, and apply idiomatic Python algorithmic enhancements before resorting to type-breaking micro-optimizations.
