# Performance & Scalability Audit Report

## 1. Codebase Profiling (CPU & Memory)

**Findings (CPU profiling via cProfile):**
- The legacy `CanaData.flatten_dictionary` recursive logic required 2,114 function calls taking ~0.002 seconds for a small batch.
- The `OptimizedDataProcessor` processes batches using Pandas DataFrames. Profiling revealed ~74,073 internal calls taking ~0.082 seconds per batch. This indicates an architectural shift away from per-item iteration toward batched DataFrame transformations.

**Findings (Memory profiling via memory_profiler):**
- The legacy iterative logic exhibited a 0.0 MiB memory increment for the test payload.
- The `OptimizedDataProcessor` exhibited a 2.0 MiB memory increment due to Pandas DataFrame overhead and series allocation.

## 2. Performance Benchmarking

A baseline suite of automated benchmarks was implemented and executed (`performance_tests/test_benchmark_processing.py`) utilizing `pytest-benchmark`.

**Latency vs Throughput:**
- **Legacy Iterative Flattening:** Demonstrated a mean execution time of ~255.65 μs per iteration, supporting roughly ~3,911 operations per second.
- **Optimized DataFrame Processor:** Exhibited a much larger mean latency of ~41.74 ms. However, this is a *batch* operation.

**Conclusion on Benchmarking:** The new `OptimizedDataProcessor` handles batched ingestion well but incurs significant DataFrame instantiation overhead. If the upstream systems produce continuous, low-latency single item data, the `OptimizedDataProcessor` will underperform.

## 3. Deep Testing & Edge Cases

A concurrency stress test (`performance_tests/test_stress_concurrency.py`) was executed, deploying 10 overlapping worker threads.

**Results:**
The test successfully managed to populate 1,000 entities in 1.27 seconds without data loss.

**Identified Risk (State Management & Race Conditions):**
The `CanaData` class manages all data directly within an internal state variable and synchronizes thread access via a single central lock:
```python
with scraper._menu_data_lock:
```
This is a "noisy neighbor" vulnerability under high horizontal load. As worker count increases, threads will spend disproportionately more time blocked awaiting lock acquisition to append to the global state. Extended distributed stress testing (`test_distributed_stress.py` via ThreadPoolExecutor) confirmed severe lock contention at high concurrency (100 workers), demonstrating measurable lock acquisition latency scaling.

## 4. Scalability Analytics & Optimization Projections

**Current Architecture:**
The system is heavily state-dependent and relies on thread locking (`_menu_data_lock`), strictly limiting it to vertical scaling on a single machine. High-concurrency tests show significant lock contention overhead.

**Optimization Projections:**

- **Before:** Global mutable array (`allMenuItems`) protected by thread locking forces synchronous write operations.
- **After (Proposed Architecture):** Moving from global state arrays to asynchronous message queues (e.g., RabbitMQ, Kafka) combined with stateless worker nodes. This will remove the `_menu_data_lock` bottleneck entirely, permitting infinite horizontal scaling and distributed processing.
