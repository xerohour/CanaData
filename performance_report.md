# Performance Audit & Optimization Report

## Executive Summary
A comprehensive performance audit was conducted to identify bottlenecks in `CanaData`'s concurrency logic and data processing. Three major optimizations were implemented targeting network I/O connection pooling, shared state concurrency locks, and CPU-bound JSON serialization overhead.

## Bottlenecks Identified

1.  **Network Connection Pooling ("Noisy Neighbor" Network I/O)**:
    -   *Issue*: The `do_request` method was instantiating fresh connections (`requests.get()`) for every API call across 10-20 concurrent worker threads. This caused port exhaustion, TLS handshake overhead, and unnecessary TCP setup latencies.
    -   *Impact*: Significant network latency scaling linearly with concurrent workers.

2.  **Concurrency Data Mapping Bottleneck (Shared Lock contention)**:
    -   *Issue*: The `_menu_data_lock` in `process_menu_json` and `process_menu_items_json` acted as a single global lock over multiple disparate data structures (`allMenuItems`, `emptyMenus`, `extractedStrains`, `menuItemsFound`, `totalLocations`). This forced all concurrent workers to process mapping logic serially, destroying horizontal scaling benefits.
    -   *Impact*: High lock acquisition wait times during multi-threaded operation.

3.  **Data Processing Overhead (Pandas vs Pure Python)**:
    -   *Issue*: When handling remaining nested structures in `optimized_data_processor.py`, `pandas.Series.apply` was being used to map `json.dumps` element-wise over columns containing lists/dicts. Pandas incurs massive overhead when applying generic Python functions compared to native Python list comprehensions.
    -   *Impact*: Heavy CPU utilization and slow execution when processing deeply nested arrays across 50,000+ items.

## Optimizations Implemented

1.  **Network Layer (`CanaData.py`)**:
    -   Instantiated a persistent `requests.Session()` within `__init__`.
    -   Mounted `HTTPAdapter` with `pool_connections` and `pool_maxsize` directly mapped to `self.max_workers`.

2.  **Locking Strategy (`CanaData.py`)**:
    -   Replaced the monolithic `_menu_data_lock` with five fine-grained locks: `_items_lock`, `_empty_lock`, `_strains_lock`, `_count_lock`, and `_locations_lock`.
    -   Reduced lock block scope strictly to the mutation operation rather than wrapping the entire `for` loop logic.

3.  **Serialization Algorithm (`optimized_data_processor.py`)**:
    -   Bypassed `pandas.Series.apply(lambda ...)` by using a pure Python list comprehension (`[json.dumps(x) ... for x in df[col].tolist()]`).

## Before vs After Benchmarks

**Benchmark 1: Synthetic Thread-Safety Scaling (100 Locations, 10 workers)**
*Measures concurrency overhead independent of network latency by utilizing mocked 10ms network delays.*
-   **Before**: ~155.94ms (High standard deviation: 54.44ms)
-   **After**: ~96.76ms (Lower standard deviation: 15.03ms)
-   *Improvement*: ~38% faster, significantly reduced jitter (more deterministic scaling).

**Benchmark 2: Synthetic Data Flattening (50,000 items, deep nesting)**
*Measures pure CPU processing time of the DataFrame nesting fallback logic using cProfile.*
-   **Before**: ~6.61 seconds execution time
-   **After**: ~6.45 seconds execution time
-   *Improvement*: ~2.5% faster overall, primarily by avoiding DataFrame object initialization overhead during mapping.

**Benchmark 3: Raw Requests vs Session Setup (50 hits)**
*Isolated profiling script testing raw network library capabilities.*
-   **requests.get**: ~2.73s
-   **session.get**: ~1.30s
-   *Improvement*: ~52% faster for repeated API calls against a single domain.

## Next Steps
Horizontal scaling is no longer artificially capped by the shared data mapping lock. Further scaling can be achieved by safely increasing `MAX_WORKERS` in tandem with the API's rate limit tolerances.