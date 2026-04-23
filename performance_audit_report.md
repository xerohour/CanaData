# Performance and Scalability Audit Report

## 1. Codebase Profiling & Benchmarks
### Dictionary Flattening Benchmark
```
Pandas processing time: 0.13s
Custom processing time: 0.05s

```
- The pandas `json_normalize` method, while general-purpose, adds structural overhead. The custom iterative stack-based algorithm (`_flatten_dictionary_custom`) is faster.

### Memory Profiling
```
Filename: profile_memory.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     4     70.8 MiB     70.8 MiB           1   @profile
     5                                         def profile_flattening():
     6     81.9 MiB     11.1 MiB       10001       test_data = [{'id': i, 'name': f'Product {i}', 'price': {'amount': 50.0, 'currency': 'USD'}, 'metadata': {'tags': ['a', 'b', 'c'], 'nested': {'deep': {'value': True}}}} for i in range(10000)]
     7     81.9 MiB      0.0 MiB           1       all_menu_items = {'loc_1': test_data}
     8     81.9 MiB      0.0 MiB           1       processor = OptimizedDataProcessor()
     9     88.7 MiB      6.8 MiB           1       processor.process_menu_data(all_menu_items)



```
- Memory usage is stable during processing.

## 2. Deep Testing & Edge Cases (Concurrency & Stress)
### Stress Test Results
```
Processed 500 locations with 50 workers in 5.09 seconds
Errors encountered: 1

```
- Stress tests confirmed `ConcurrentMenuProcessor` handles high concurrency and properly traps exceptions.
- The global rate limit lock effectively prevents API bans but creates a mild bottleneck at high worker counts.

## 3. Scalability Analytics
## Architectural Analysis
- **Threading Model**: Multithreading via ThreadPoolExecutor.
- **Shared State**: The global rate limit is enforced without creating a concurrency bottleneck by calculating the next allowed execution time inside a shared lock, then releasing the lock before calling time.sleep().

- For true horizontal scaling, transitioning to multiprocessing or a distributed task queue (like Celery) would be necessary.

## 4. "Before vs. After" Optimization Projection
- **Before**: Pandas normalization is slow for large payloads.
- **After**: Prioritizing the custom stack algorithm significantly reduces flattening time.
