# Performance & Scalability Audit Report

## 1. Codebase Profiling (Memory & CPU)
**Methods:**
- Memory profiling was conducted using `cProfile` and `psutil` via `scripts/profile_memory_leaks.py` to identify bottlenecks during high-volume simulated data ingestion (10x product multiplier).
- Legacy recursive flattening vs Pandas optimized flattening was compared.

**Findings:**
- Initial memory footprint: ~94.23 MB
- Final memory footprint post-GC: ~96.86 MB (Delta: 2.62 MB)
- Memory allocation scales linearly with dataset size; no severe, unbounded memory leaks were detected in the Python data processing layer, provided proper garbage collection.
- However, profiling shows that `optimized_data_processor.py` continues to spend significant cumulative time in Pandas DataFrame serialization and normalization functions (e.g., `_normalize_data`, `to_dict`, `json_normalize`).

## 2. Performance Benchmarking
Automated benchmarks (`performance_tests/test_audit_benchmarks.py`) using `pytest-benchmark` were executed on the core data processing methods (10x scaled sample data).

**Latency vs Throughput Results:**
- **Legacy Iterative Flattening (`test_legacy_flattening_latency`):** Mean execution time ~2.63 ms per batch. High throughput (~380 OPS) due to simplistic memory assignment, but scales linearly and poorly with deep nesting.
- **Optimized DataFrame Processor (`test_optimized_flattening_latency`):** Mean execution time ~31.91 ms per batch. Throughput is significantly lower (~31 OPS).
- *Observation:* While Pandas processing was previously "optimized" (reducing execution time from 37.5ms to 25.1ms in earlier audits), it still introduces massive overhead (approx 10x slower on 10x data size) compared to raw dictionary iterations for relatively flat structures. Pandas is highly inefficient for this specific workload configuration.

## 3. Deep Testing & Scalability Analytics (Distributed Systems)
A stress test (`performance_tests/test_audit_stress.py`) simulating high-concurrency (25 threads, 12,500 operations total) state writing into `CanaData` was executed.

**Findings:**
- **State Synchronization (`test_high_concurrency_state_write`):** Mean execution time ~23.43 ms per 12,500 operations (~42.7 OPS).
- The `_menu_data_lock` successfully prevents race conditions and data corruption.
- As previously concluded, the fast O(1) dictionary assignments inside the global lock are *not* a severe vertical scalability bottleneck.
- **Architectural Scalability Limitation:** Despite the lock not being a vertical bottleneck, the current architecture strictly binds state (`scraper.allMenuItems`) to the process memory of the `CanaData` instance.

## 4. Optimization Projections (Before vs. After)

### Current Architecture (Before)
- **State Management:** Monolithic and stateful. All scraped data and configurations live in process RAM within the `CanaData` instance, protected by thread locks.
- **Scaling:** Limited strictly to Vertical Scaling (scaling up the VM/container resources). It is impossible to horizontally scale to multiple instances because they do not share the central `allMenuItems` state dictionary.
- **Processing:** The Pandas `OptimizedDataProcessor` introduces 10x latency overhead compared to raw dictionary traversal for the current payload structures.

### Proposed Architecture (After)
1. **Stateless Worker Nodes (Horizontal Scaling):**
   - Refactor `CanaData` to be entirely stateless.
   - Introduce an external message broker (e.g., RabbitMQ, Kafka, or Redis Queue).
   - Workers will pull URLs/slugs from the queue, fetch data, and immediately push the raw JSON payload to a downstream processor queue.
2. **Decoupled Processing & Storage:**
   - A dedicated aggregation service will consume the raw data queue, perform the JSON flattening (dropping Pandas in favor of optimized recursive Cython or raw Python dict unions), and stream it directly to a database or blob storage, eliminating the need for process-bound arrays entirely.
3. **Projected Impact:**
   - **Throughput:** Infinite horizontal elastic scaling.
   - **Latency:** Elimination of Pandas initialization overhead, resulting in 10x faster batch processing.
   - **Reliability:** Message queues provide automatic retries and dead-lettering, removing the risk of data loss from node crashes.
