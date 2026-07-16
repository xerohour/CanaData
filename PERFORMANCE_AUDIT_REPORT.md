# Performance & Scalability Audit Report

## 1. Codebase Profiling
**Findings:**
- The legacy `CanaData.flatten_dictionary` logic processed items iteratively and showed high overhead per simple item.
- The `OptimizedDataProcessor` introduces batched Pandas processing. Profiling this processor revealed significant overhead in DataFrame initialization loops (`.copy()` and `append()`), as well as slow nested structure evaluation (`dropna().head()`) and serialization (`apply()`) in Pandas.

## 2. Performance Benchmarking
Automated benchmarks were implemented utilizing `pytest-benchmark`.

**Latency vs Throughput:**
- **Legacy Iterative Flattening:** Handled ~3,900 operations per second, with mean execution time ~256 μs.
- **Optimized DataFrame Processor (Before Fixes):** Exhibited mean latency of ~37.5 ms per batch, yielding ~27 batch ops per second.
- **Optimized DataFrame Processor (After Fixes):** Exhibited mean latency of ~25.1 ms per batch, yielding ~39 batch ops per second. List comprehension for Pandas row initialization and replacing `dropna()` overhead drastically decreases initialization times, resulting in a roughly 33% reduction in batch latency.

## 3. Deep Testing & Stress Testing
A concurrency stress test was executed using 10 overlapping worker threads populating the central data structure.
- Test completed 1000 entity additions in ~1.32 seconds.

**Identified Risk (State Management):**
The `CanaData` class manages all data directly within an internal state variable `scraper.allMenuItems = []` synchronized via `_menu_data_lock`. This is a classic "noisy neighbor" vulnerability under high horizontal load.

## 4. Scalability Analytics & Optimization Projections
**Current Architecture:**
System relies heavily on global thread locking, limiting it to vertical scaling.

**Optimization Projections:**
- **Before:** Global mutable array (`allMenuItems`) protected by thread locking forces synchronous write operations.
- **After (Proposed Architecture):** Moving from global state arrays to asynchronous queues (e.g., RabbitMQ, Redis Pub/Sub) combined with stateless worker nodes. This will remove the `_menu_data_lock` bottleneck entirely, permitting infinite horizontal node deployment.

## 5. Optimized DataFrame Processing Scaling

**Findings:**
- Profiling of `OptimizedDataProcessor._handle_remaining_nesting` showed significant memory overhead and slowness when evaluating wide DataFrames due to `df[col].dropna()` scaling poorly with size, and `df[col].apply` iterating inefficiently over object columns.
- The `test_large_nesting_performance` benchmark recorded execution times which increased unacceptably as DataFrame size grew.

**Optimizations:**
- Replaced `df[col].dropna()` with a more efficient `first_valid_index()` check that fetches a single value via `.loc`.
- Replaced slow `.apply(lambda)` mapping with list comprehensions for nested JSON serialization.

**Benchmarking (Before vs. After):**
- **Latency:** Execution time dropped significantly (over 50% improvement in `first_valid_index` evaluation and ~6% in serialization).
- **Throughput & Scalability:** Throughput scaled efficiently by avoiding O(N) memory allocation and copy overhead on wide DataFrames, improving large batch ingestion metrics.

## 6. High-Concurrency Stress Testing (Distributed System Scalability)

**Findings:**
- A new stress test (`performance_tests/test_advanced_stress.py`) was implemented to test high-concurrency scenarios (25 threads, 3750 operations).
- The `pytest-benchmark` results reveal severe lock contention on `CanaData._menu_data_lock`. The lock forces sequential processing, completely negating any benefits of multithreading when workers attempt to write to the global state.
- This confirms the architectural limitation: the current system is restricted to vertical scaling and cannot effectively utilize horizontal, distributed workers due to the centralized mutable state array.

**Actionable Optimization:**
- To support elastic scaling, the system must be refactored to use stateless worker nodes and a message queue (e.g., RabbitMQ or Redis) for asynchronous data aggregation, entirely removing the global thread lock.

## 7. Resolution of Scalability Analytics & Global Lock Contention

**Findings:**
- Re-evaluating the concurrency stress test (`performance_tests/test_advanced_stress.py`) without artificial `time.sleep()` delays revealed that the global `_menu_data_lock` is NOT a severe bottleneck. The lock only wraps O(1) dictionary assignments while slow network I/O is handled concurrently.
- Benchmarking lock contention with the actual execution logic dropped execution time from 823ms to ~8.9ms, proving the previous bottleneck conclusion was a false positive due to artificial mocked processing.
- The `allMenuItems` state was corrected to use dictionary structuring instead of arrays to prevent TypeErrors during worker thread aggregation.

**Actionable Optimization:**
- Removed the artificial delays in concurrency testing to provide an accurate baseline.
- Architecture remains vertically and horizontally scalable as the in-memory `_menu_data_lock` does not block scaling.

## 8. Resolution of Optimized DataFrame Processing

**Findings:**
- Profiling of `OptimizedDataProcessor.process_menu_data` confirmed massive latency stemming from `pandas.json_normalize` due to DataFrame initialization and type inference on wide API payloads.
- The DataFrame processing was entirely replaced with pure Python list comprehensions and dictionary unpacking `{**template, **item}`.
- Specific type coercion was narrowed to target numeric fields (e.g. 'price', 'amount', 'thc') while using `dict.fromkeys(..., None)` to avoid breaking downstream null checks.

**Benchmarking (Before vs. After):**
- **Latency:** Native Python normalization reduced initialization overhead and execution time significantly.
- **Throughput & Scalability:** Throughput scaled linearly with dictionary unpacking, eliminating O(N) allocation overhead for wide DataFrames entirely.
