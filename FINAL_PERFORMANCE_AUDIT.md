# Performance Audit Report

## 1. Codebase Profiling
**Findings:**
- Based on `cProfile` outputs (`run_profiler.py`), the `OptimizedDataProcessor`'s Pandas normalization remains a bottleneck.
- The `process_menu_data` spends significant time within Pandas internal functions such as `_normalize_json`, `to_dict`, and array casting (`maybe_box_native`).
- Initializing wide dataframes and object type inference continue to introduce substantial CPU overhead on the single-threaded dataframe flattening execution.

## 2. Performance Benchmarking
**Metrics:**
- Legacy processing throughput: ~4,800 operations per second.
- Optimized Pandas batch throughput: ~48 batch operations per second.
- While Pandas batch processing is vastly superior for data transformation consistency, it currently scales poorly for deeply nested flattening.

## 3. Deep Testing & Edge Cases
- Implemented `test_failure_modes.py` mapping simulations of API timeouts and testing the thread-safety of the internal `CacheManager`. Tests verified `CanaData` safely swallows exceptions to prevent pipeline crashes.
- Implemented `test_race_conditions.py` which rigorously executes thread racing.

## 4. Scalability Analytics
- **Architecture Scalability:** High-concurrency tests (`test_high_concurrency_race_conditions` & `test_high_concurrency_global_lock_contention`) definitively proved severe thread lock contention. The shared global mutable array `scraper.allMenuItems`, protected by `_menu_data_lock`, forces sequential writing. Performance aggressively degrades as concurrent worker threads scale.
- **Optimization Projection:**
  - **Before:** Global state arrays protected by thread locking, artificially limiting the system to vertical scaling and introducing "noisy neighbor" latency.
  - **After (Recommended Solution):** Transition `CanaData` architecture from a shared global array to a distributed message queue (e.g., RabbitMQ, Kafka) paired with stateless worker components. This decoupling will eliminate the central lock bottleneck and facilitate boundless horizontal elasticity.
