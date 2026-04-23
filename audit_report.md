# CanaData Performance & Scalability Audit Report

## 1. Executive Summary
This technical audit evaluated the `CanaData` repository focusing on deep testing, performance benchmarking, algorithmic scalability, and concurrency safety.

### Key Discoveries
- **Algorithmic Bottleneck (False Assumption):** Counter-intuitively, the existing custom stack-based recursive flattener (`CanaData.flatten_dictionary`) vastly outperforms the newly implemented Pandas-based `OptimizedDataProcessor`.
- **Concurrency & Scaling:** The API architecture successfully scales horizontally to concurrent processing. Shared data mutations (`allMenuItems`, `totalLocations`) are properly protected by `threading.Lock()` (`self._menu_data_lock`), ensuring thread safety without data loss.

---

## 2. Codebase Profiling
We used `cProfile` and `memory_profiler` to trace execution time and memory allocation while flattening a mock dataset of 20 locations (1,000 deeply nested menu items).

### Raw Data (`profile_results.txt`):
**Custom Flattening (`flatten_dictionary`)**
- Total Time: `0.618s`
- Memory Increment: `~1.0 MiB` peak usage.

**Optimized Flattening (`OptimizedDataProcessor` with Pandas)**
- Total Time: `0.863s`
- Memory Increment: `~2.4 MiB` peak usage.

**Finding:** The custom iterative stack-based implementation avoids the high memory overhead and initialization penalty of instantiating `pandas.DataFrame` and running `pandas.json_normalize`. The "Optimized" processor is actually `~39%` slower and uses `2.4x` the memory.

---

## 3. Performance Benchmarking
Micro-benchmarks via `pytest-benchmark` were run to isolate the critical paths.

### Raw Data (`benchmark_results.txt`):
| Method | Min Latency (μs) | Mean Latency (μs) | Operations / Sec |
| :--- | :--- | :--- | :--- |
| `custom_flattening (batch)` | 21,242.1 | 22,622.0 | 44.2 |
| `optimized_flattening (batch)` | 54,827.7 | 56,594.2 | 17.6 |
| `flatten_dictionary (single)` | 11.1 | 12.4 | 80,365.3 |
| `_flatten_dictionary_custom (single)`| 12.8 | 14.4 | 69,223.6 |

**Finding:** The custom implementation yields `80K OPS` compared to the pandas-fallback algorithm at `69K OPS`. When processing large batches (e.g., 1000 items), the custom iterative method provides a 2.5x throughput multiplier over the full Pandas pipeline.

---

## 4. Deep Testing & Edge Cases
Stress tests were implemented targeting thread safety and distributed system failure modes (`tests/test_concurrency.py`).

### Thread Safety Analysis
- **`ConcurrentMenuProcessor`:** Uses a `ThreadPoolExecutor` and correctly maps tasks. If an individual API request fails (simulated via `ValueError`), the error is safely caught and appended to `processor.errors` without crashing the thread pool or dropping other successful requests.
- **`CanaData` internal state:** Under high concurrency (10 threads), writing to `self.allMenuItems`, `self.totalLocations`, and `self.finishedMenuItems` resulted in 0 dropped rows or race conditions, thanks to the proper use of `self._menu_data_lock` during mutation blocks.
- **`CacheManager`**: Write-heavy concurrent workloads generated successful memory cache hits without deadlocking or raising `KeyError` (verified across 1,000 mock concurrent requests).

---

## 5. Scalability Analytics

### Horizontal Scalability Constraints
1. **Connection Pooling Bottleneck:** The `requests.Session()` within `CachedAPIClient` is not configured with an explicit connection pool size matching `MAX_WORKERS`. By default, `requests` uses a pool size of 10. If `MAX_WORKERS` is set to 50, threads will block waiting for connections to free up, resulting in synthetic latency.
2. **"Noisy Neighbor" Risk (Memory Cache):** The current `CacheManager` stores unstructured JSON in an unbounded dictionary (`self.cache` inside the thread). In containerized environments, massive scrapes (e.g., California `searchSlug`) could trigger Out-Of-Memory (OOM) kills on pods with strict memory limits, despite the `memory_cache_size` param, because the dictionary tracks items, not byte-size.

---

## 6. Projections & Optimization Roadmap

### Before vs. After Projection

| Metric | Current State | Projected State (Post-Opt) | Expected Gain |
| :--- | :--- | :--- | :--- |
| Data Processing Speed | ~56ms / 1K items | ~22ms / 1K items | **~2.5x Faster** |
| Memory Allocation | 2.4 MiB / 1K items | 1.0 MiB / 1K items | **-58% Memory** |
| High-Concurrency Latency| Threads blocked on connections | Zero connection blocking | **Eliminates thread starvation** |

### Recommendations for Engineering Teams
1. **Deprecate Pandas Dependency:** The `OptimizedDataProcessor` should be removed, and `CanaData` should permanently default to `optimize_processing=False`. This eliminates the heavy `pandas` dependency and improves raw throughput.
2. **Mount HTTP Adapters:** Update `requests.Session()` to mount `requests.adapters.HTTPAdapter(pool_connections=MAX_WORKERS, pool_maxsize=MAX_WORKERS)` to prevent socket starvation under high concurrency.
3. **Container-Aware Caching:** Implement a bounded LRU cache based on byte-size estimation rather than raw item counts for the memory cache to prevent Docker OOM kills.
