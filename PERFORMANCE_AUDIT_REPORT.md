# Performance & Scalability Audit Report

## 1. Codebase Profiling

**Findings:**
- A substantial bottleneck existed within the legacy `CanaData.flatten_dictionary` recursive logic. Profiling showed 1,194 function calls taking 0.003 seconds for simple JSON objects when operating in `optimize_processing=False` mode.
- The newly introduced `OptimizedDataProcessor` processes batches utilizing Pandas DataFrames. Profiling this processor revealed initialization overhead. This clearly indicates an architectural shift away from per-item iteration toward batched DataFrame transformations, making throughput highly dependent on `chunk_size` and memory availability.

## 2. Performance Benchmarking

A baseline suite of automated benchmarks was executed (`performance_tests/test_benchmark_processing.py`) utilizing `pytest-benchmark`.

**Latency vs Throughput:**
- **Legacy Iterative Flattening:** The baseline `CanaData.flatten_dictionary` showed a mean execution time of ~268 μs per iteration, supporting roughly ~3,700 operations per second.
- **Optimized DataFrame Processor:** The `OptimizedDataProcessor.process_menu_data` exhibited a much larger mean latency of ~37.7 ms per batch. However, this is a *batch* operation. The legacy system operates iteratively (item by item), whereas the new processor handles bulk DataFrame ingestion.

**Conclusion on Benchmarking:** The new `OptimizedDataProcessor` handles batched ingestion well but incurs significant DataFrame instantiation overhead (notably `pandas/core/internals`). If the upstream systems produce continuous, low-latency single item data, the `OptimizedDataProcessor` will underperform due to initialization overhead.

## 3. Deep Testing & Stress Testing

A concurrency stress test (`performance_tests/test_stress_concurrency.py`) was executed, deploying 10 overlapping worker threads that aggressively populate the central data structure.

**Results:**
The test successfully managed to populate 1,000 entities in 0.84 seconds without data loss.

**Identified Risk (State Management):**
The `CanaData` class manages all data directly within an internal state variable:
```python
scraper.allMenuItems = []
```
And synchronizes thread access via a single central lock:
```python
with scraper._menu_data_lock:
```
This is a classic "noisy neighbor" vulnerability under high horizontal load. As worker count increases, threads will spend disproportionately more time blocked awaiting lock acquisition to append to the global state.

## 4. Scalability Analytics & Optimization Projections

**Current Architecture:**
The system is heavily state-dependent and relies on thread locking (`_menu_data_lock`), strictly limiting it to vertical scaling on a single machine.

**Optimization Projections:**

- **Before:** Global mutable array (`allMenuItems`) protected by thread locking forces synchronous write operations.
- **After (Proposed Architecture):** Moving from global state arrays to asynchronous queues (e.g., RabbitMQ, Redis Pub/Sub) combined with stateless worker nodes. This will remove the `_menu_data_lock` bottleneck entirely, permitting infinite horizontal node deployment.
