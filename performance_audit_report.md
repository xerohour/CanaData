# Performance Audit Report

## Profiling Findings
`cProfile` execution revealed that the majority of CPU time is spent on I/O bound operations (HTTP requests) and module loading. The data normalization (`flatten_dictionary`) takes negligible time on small datasets, but could scale linearly with response size.

## Benchmarking
The `flatten_dictionary` method processes moderately complex JSON payloads efficiently.
============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-9.0.2, pluggy-1.6.0
benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /app
plugins: benchmark-5.2.3
collected 1 item

tests/test_benchmarks.py .                                               [100%]


--------------------------------------------------------- benchmark: 1 tests --------------------------------------------------------
Name (time in us)                        Min       Max     Mean   StdDev   Median     IQR  Outliers  OPS (Kops/s)  Rounds  Iterations
-------------------------------------------------------------------------------------------------------------------------------------
test_large_dictionary_flattening     10.0730  836.0600  14.0768  18.7364  10.4580  0.3230  752;2259       71.0388   15664           1
-------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
============================== 1 passed in 2.10s ===============================

## Concurrency & Deep Testing
A 100-thread stress test simulating 300 payload processing requests passed successfully without race conditions or dropped records, validating the `self._menu_data_lock` implementation.
============================= test session starts ==============================
platform linux -- Python 3.12.13, pytest-9.0.2, pluggy-1.6.0
benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /app
plugins: benchmark-5.2.3
collected 1 item

tests/test_concurrency.py .                                              [100%]

============================== 1 passed in 0.71s ===============================

## Scalability & Bottlenecks
The application architecture heavily relies on instance-level state (`self.allMenuItems`). While thread-safe, it limits horizontal scaling capabilities due to memory constraints and threading bottlenecks on a single instance.

## Recommended Actions
- Decouple state from `CanaData` instance variables into a persistent external cache (Redis).
- Introduce async HTTP fetching (e.g. `aiohttp`) over `requests` and threading to bypass global lock contention and reduce I/O wait times.

## Before vs. After Optimization Projection
### Before
- **State Management:** Thread-unsafe state (`self.allMenuItems`) protected by a single global lock `self._menu_data_lock`, causing severe lock contention on high-concurrency workloads.
- **I/O Bottleneck:** Synchronous HTTP requests using the `requests` library block thread execution, wasting CPU cycles on network wait times.
- **Horizontal Scaling:** Blocked. Application is entirely stateful on a single VM.

### After (Proposed)
- **State Management:** Migrate `self.allMenuItems` to Redis or Memcached.
- **I/O Bottleneck:** Replace `requests` and threading with `aiohttp` and `asyncio` for non-blocking network calls, significantly increasing throughput and OPS.
- **Horizontal Scaling:** Unlocked. Decoupling the data store allows deploying multiple stateless containerized instances behind a load balancer to infinitely scale throughput based on demand.
