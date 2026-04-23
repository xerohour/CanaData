# Performance Audit Report

## 1. Codebase Profiling
- Identified that synchronous HTTP requests block threads, causing high latency due to I/O constraints (socket blocking).
- Analyzed cProfile statistics generated during profile script run showing dominant bottleneck on network requests.

## 2. Performance Benchmarking
- Captured performance of custom recursive flattening vs pandas json_normalize through pytest-benchmark.
- The custom recursive flattening is actually much faster (mean ~15 us) than pandas json_normalize (mean ~3076 us) for the typical payload size, mainly due to pandas overhead.

## 3. Deep Testing & Edge Cases
- Tested concurrency logic in `ConcurrentMenuProcessor` verifying thread locks protect data mutations without crashing.

## 4. Scalability Analytics
- The architecture limits horizontal scalability due to in-memory state (`self.allMenuItems`, `self.totalLocations`).
- Recommendation: Shift to `aiohttp` and `asyncio` for HTTP requests. Use distributed caches (e.g., Redis) instead of file-based/in-memory caches.

## 5. Before vs. After Optimization Projection
- **Before:** I/O blocking limits concurrent execution to the number of threads. High peak memory due to state accumulation in single class.
- **After:** Async architecture allows near-limitless connection concurrency, maximizing throughput per node. Dropping internal state lowers memory footprint enabling multi-node scalability.
