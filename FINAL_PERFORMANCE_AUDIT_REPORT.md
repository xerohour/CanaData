# Comprehensive Performance & Scalability Audit Report

## 1. Codebase Profiling
**Observation**:
The core engine `CanaData` relies heavily on an internal mutable state dictionary `self.allMenuItems` which is accessed by multiple concurrent worker threads across the application. `ConcurrentMenuProcessor` implements rate-limiting functionality.
**Bottlenecks Identified**:
- **Thread Locking overhead**: The `_menu_data_lock` in `CanaData.py` forces threads to block sequentially on writes.
- **Synchronous Queueing in `ConcurrentMenuProcessor`**: The rate limiter uses `threading.Lock()` via `self.request_lock` inside `_wait_for_rate_limit()` which creates a global stop-the-world condition for all workers, preventing true asynchronous dispatch.

## 2. Performance Benchmarking
Using `pytest-benchmark`, we measured throughput:
- **Lock Contention Throughput**: The `test_throughput_batch_size` benchmark demonstrated that list appending under the `_menu_data_lock` executes rapidly per batch, but limits concurrent scaling when many threads compete.

## 3. Deep Testing & Edge Cases
- **High-Concurrency Race Conditions**: The `test_high_concurrency_race_condition` stress test with 30 overlapping threads pushing 6000 items confirmed that while the lock prevents data corruption (no lost updates), the processing time balloons unacceptably due to lock contention.
- **Rate-Limiting Bottleneck**: `test_concurrent_processor_rate_limit` confirmed that the shared rate-limiting lock correctly throttles execution.

## 4. Scalability Analytics & Projections
**Current Architecture Constraints**:
The application employs an in-memory vertical scaling pattern. `CanaData` acts as a stateful monolith, holding the entire dataset in `self.allMenuItems` and `self.totalLocations`.

**Before vs After Optimization Projection**:
- **Before**: A single process with `N` threads. As `N` increases, lock contention on `_menu_data_lock` and the rate limiter decreases total throughput, leading to a hard cap on performance. Memory scales linearly with dataset size in a single node, risking OOM kills.
- **After (Proposed)**: Decouple the scraper into stateless worker nodes. Replace `_menu_data_lock` and in-memory lists with an external message broker (e.g., Redis Streams or RabbitMQ).
- **Impact**: Removing in-memory state permits elastic horizontal scaling (deploying infinite Docker containers), removes Python Global Interpreter Lock (GIL) and custom threading lock limitations, and drastically improves system resilience against node failure.
