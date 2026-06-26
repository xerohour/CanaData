# Performance & Scalability Audit Report

## 1. Codebase Profiling

**Findings:**
- Initial profiling of `CanaData.flatten_dictionary` with legacy settings over `sample_products.json` revealed:
  - Total function calls: 2106
  - `cumtime` for `flatten_dictionary`: 0.001 seconds
  - Redundant O(n) calls: 50 calls to `{method 'keys' of 'dict' objects}` and 60 calls to `len()`
- **After Optimization (Replaced O(n) checks with O(1) truthiness):**
  - Total function calls dropped to 1996, effectively removing the 110 redundant operations over the exact same dataset.

## 2. Performance Benchmarking

Baseline metrics collected using `pytest-benchmark`:

**Latency vs Throughput (Before Optimization):**
- **Legacy Iterative Flattening:** Mean latency 324.03 μs per call, supporting 3,086.13 operations per second.
- **Optimized DataFrame Processor:** Mean latency 43,938.76 μs per batch. Handles batched ingestion well but incurs significant initialization overhead.

**Latency vs Throughput (After Truthiness Optimization):**
- **Legacy Iterative Flattening:** Mean latency 251.20 μs per call, supporting 3,980.76 operations per second. This is an improvement of ~28% in throughput.

## 3. Deep Testing & Stress Testing

A concurrency stress test (`performance_tests/test_stress_concurrency.py`) was executed.

**Results:**
- Test completed successfully in 1.34s, managing 1,000 entity writes.

**Identified Risk (State Management):**
The system relies on a central global array `scraper.allMenuItems` protected by `scraper._menu_data_lock`. Under heavy concurrent load, threads will block waiting to acquire the lock. This is a severe "noisy neighbor" vulnerability that will degrade performance as concurrency increases.

## 4. Scalability Analytics & Optimization Projections

**Current Architecture:**
The architecture relies entirely on vertical scaling (threading on a single machine) because it aggregates all scraped data into local state via `_menu_data_lock`.

**Optimization Projections:**

- **Current State:** Global mutable state synchronized via thread locking. Synchronous I/O operations block worker threads.
- **Proposed Architecture:**
  - Shift to a stateless worker model where each worker acts independently.
  - Implement asynchronous Message Queues (e.g., RabbitMQ, Redis) for data ingestion, completely removing `_menu_data_lock`.
  - Use a distributed data store (e.g., MongoDB, PostgreSQL) for final data aggregation instead of holding it all in memory.