# System Performance and Scalability Audit Report

## 1. Codebase Profiling & Analysis
**Findings:**
- Based on `cProfile` and `memory_profiler` executions targeting `CanaData.organize_into_clean_list`, the overall flattening architecture heavily relies on Pandas (`json_normalize`).
- Over 85% of time is spent deeply nested in Python internal and Pandas methods rather than business logic.
- Total parsing overhead takes ~0.077 seconds per 500 entity batch, which is reasonably fast for vertical architectures but CPU-intensive during scale.
- Memory usage remained stable at ~98.8 MiB for processing during standard flattening batches indicating no immediate local memory leaks within the flattening pipeline.

## 2. Performance Benchmarking
Automated benchmarks were executed using `pytest-benchmark`.
**Latency vs Throughput:**
- **Legacy Iterative Flattening:** Handled ~3,816 operations per second, with mean execution time ~262 μs.
- **Optimized DataFrame Processor:** Exhibited mean latency of ~25.8 ms per batch, yielding ~38.7 batch ops per second.
- **High Concurrency Global Lock Contention:** Exhibits ~14.04 ms response handling 25 overlapping threads writing 3750 operations.
- **System Audit High Concurrency:** ~78-80 ms response handling 50 overlapping threads writing 25,000 entities.

## 3. Deep Testing, Stress Testing & Architecture Scalability
A specific stress test (`test_distributed_architecture_bottleneck`) was implemented to test high-concurrency distributed architectural scenarios involving simulated I/O bound blocking.
- **Test execution:** ~143.3 ms mean latency, capping throughput to just ~6.9 operations per second.

**Identified Risk (State Management / Horizontal Scaling):**
- **"Noisy Neighbor" Vulnerability:** The `CanaData` architecture currently relies entirely on an internal memory array `scraper.allMenuItems` for storing and grouping location items. It handles synchronization for thread concurrency via the `_menu_data_lock`.
- While perfectly sufficient for single-machine, vertical multi-threading (where in-memory `dict.update()` operations are functionally instantaneous), this tightly coupled state severely degrades under distributed horizontal scaling scenarios (deploying multi-node container architectures) since the lock inherently forces sequential operations across the global state pool.

## 4. Scalability Optimization Projections
**Current Architecture:**
Monolithic class state relying on global thread locking, inherently limiting scaling to vertical compute boundaries.

**"Before vs. After" Optimization Projection:**

* **Before (Current):**
  - **Architecture:** Monolithic, stateful worker execution.
  - **Bottleneck:** `_menu_data_lock` serializes data ingestion; memory limits constrain max concurrent processes.

* **After (Proposed Architecture):**
  - **Architecture:** Event-driven, stateless worker nodes.
  - **Implementation Strategy:** Move away from global mutable arrays (`allMenuItems`) toward asynchronous message queues (e.g., RabbitMQ, Kafka, or Redis Pub/Sub).
  - **Impact:** Decoupling scraper nodes from data aggregation eliminates the `_menu_data_lock` bottleneck entirely. This will allow infinite elastic horizontal scaling where the system can immediately spin up hundreds of transient, containerized workers to process large state loads simultaneously without any cross-thread blocking.