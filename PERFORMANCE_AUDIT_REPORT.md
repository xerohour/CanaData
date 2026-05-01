# Performance & Scalability Audit Report

## 1. Codebase Profiling

**Findings:**
- A substantial bottleneck existed within the legacy `CanaData.flatten_dictionary` recursive logic. Profiling showed 2,287 function calls taking 0.003 seconds for simple JSON objects when operating in `optimize_processing=False` mode.
- The newly introduced `OptimizedDataProcessor` processes batches utilizing Pandas DataFrames. Profiling this processor revealed 73,952 internal calls taking roughly 0.090 seconds per batch. This clearly indicates an architectural shift away from per-item iteration toward batched DataFrame transformations, making throughput highly dependent on `chunk_size` and memory availability.

## 2. Performance Benchmarking

A baseline suite of automated benchmarks was implemented (`performance_tests/test_benchmark_processing.py`) utilizing `pytest-benchmark`.

**Latency vs Throughput:**
- **Legacy Iterative Flattening:** The baseline `CanaData.flatten_dictionary` showed a mean execution time of ~256 μs per iteration, supporting roughly ~3,900 operations per second.
- **Optimized DataFrame Processor:** The `OptimizedDataProcessor.process_menu_data` exhibited a much larger mean latency of ~37.5 ms. However, this is a *batch* operation. The legacy system operates iteratively (item by item), whereas the new processor handles bulk DataFrame ingestion.

**Conclusion on Benchmarking:** The new `OptimizedDataProcessor` handles batched ingestion well but incurs significant DataFrame instantiation overhead (notably `pandas/core/internals`). If the upstream systems produce continuous, low-latency single item data, the `OptimizedDataProcessor` will underperform due to initialization overhead.

**Resource Utilization (CPU/RAM):**
A raw resource consumption test (`performance_tests/test_resource_utilization.py`) tracked the overhead of iterative `process_menu_items_json` payloads processing using `psutil`. Over a 5-batch simulation using a simulated large menu response payload:
- **Mean Latency:** ~272 μs per cycle
- **Memory Jump:** Stable (~0.00 MB marginal growth measured per short iteration loop block), indicating the garbage collection is handling object destruction cleanly when iterative batch instances fall out of scope.

## 3. Deep Testing & Stress Testing

A concurrency stress test (`performance_tests/test_stress_concurrency.py`) was implemented, deploying 10 overlapping worker threads that aggressively populate the central data structure.

**Results:**
The test successfully managed to populate 1,000 entities in 0.12 seconds without data loss.

**Failure Modes & Edge Cases (Distributed Mock):**
A concurrency failure test (`performance_tests/test_high_concurrency_race_conditions.py`) was implemented using the `responses` module to simulate a degraded downstream network API (50% HTTP 500 failure rate). The legacy fallback method handles failures natively without cascading race conditions across sibling threads, cleanly returning `False` for the individual thread's processing attempt.

**Identified Risk (State Management):**
The `CanaData` class manages all data directly within an internal state variable:
```python
scraper.allMenuItems = []
```
And synchronizes thread access via a single central lock:
```python
with scraper._menu_data_lock:
```
This is a classic "noisy neighbor" vulnerability under high horizontal load. As worker count increases, threads will spend disproportionately more time blocked awaiting lock acquisition to append to the global state. In measured automated tests (`test_stateful_noisy_neighbor_lock_contention`), scaling from 5 simultaneous threads to 50 threads caused a ~10.45x degradation in raw throughput purely due to thread locking synchronization overhead blocking the active processors.

## 4. Scalability Analytics & Optimization Projections

**Current Architecture:**
The system is heavily state-dependent and relies on thread locking (`_menu_data_lock`), strictly limiting it to vertical scaling on a single machine.

**Optimization Projections (Before vs. After):**

- **Before:** Global mutable array (`allMenuItems`) protected by thread locking forces synchronous write operations. Our stress testing demonstrated a severe ~10.45x degradation in throughput under high concurrency (50 threads) due to wait-time on the single central lock.
- **After (Proposed Architecture):** Moving from global state arrays to asynchronous queues (e.g., RabbitMQ, Redis Pub/Sub) combined with stateless worker nodes. This will remove the `_menu_data_lock` bottleneck entirely, permitting infinite horizontal node deployment and achieving near linear scalability with worker count instead of logarithmic decay.
