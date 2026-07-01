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
- **Before:** Global mutable array protected by locks forces synchronous writes.
- **After (Proposed Architecture):** Moving to asynchronous queues (e.g., RabbitMQ, Redis) combined with stateless worker nodes will remove the lock bottleneck entirely. Code-level Pandas optimizations implemented in this patch significantly lower batch processing latency, enabling higher throughput within each node.
