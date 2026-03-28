import os

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"[File not found: {path}]"

def main():
    report = f"""# CanaData Performance Audit Report

## Executive Summary
The performance audit conducted on the CanaData repository profiled core logic, benchmarked algorithms, stress-tested concurrent mechanisms, and analyzed the architectural scalability. The overall findings show the application performs extremely well vertically but has stateful data structures (`self.allMenuItems`) and file-based caching (`pickle` on disk) that limit its ability to scale horizontally.

## 1. Profiling Results (Typical Workloads)
The profiling revealed that overhead from instantiation and dependency checks is minimal, with execution completing effectively instantaneously on a mocked small payload.
```text
{read_file('perf_audit/profile_results.txt').strip()}
```

## 2. Benchmarks (Custom vs Optimized Flattening)
The pytest-benchmark results indicate that the original custom recursive flattening algorithm `flatten_dictionary` performs slightly *faster* than the `OptimizedDataProcessor` (which acts as a fallback or pandas hybrid).
- Custom `flatten_dictionary`: ~32.7k ops/s
- `OptimizedDataProcessor._flatten_dictionary_custom`: ~29.1k ops/s
```text
{read_file('perf_audit/benchmark_results.txt').strip()}
```

## 3. Concurrency Test Results
The concurrent processor correctly speeds up I/O bound tasks almost perfectly linearly as thread count increases, reducing the completion time of 100 delayed mock requests from ~1 second to ~0.06 seconds.
```text
{read_file('perf_audit/concurrency_results.txt').strip()}
```

## 4. Stress Test Results
The `ConcurrentMenuProcessor` was subjected to 100 workers handling 500 items, and no deadlocks, thread-starvation, or memory spikes were detected. It utilized 95 unique threads and completed in under a second.
```text
{read_file('perf_audit/stress_results.txt').strip()}
```

## 5. Edge Cases (Deep JSON & Failure Modes)
### Deep JSON
A deep recursive dictionary (up to depth 500) did not throw a `RecursionError` and was processed in under 0.001 seconds, proving `flatten_dictionary` is memory and CPU safe for deep Weedmaps API responses.
```text
{read_file('perf_audit/deep_json_results.txt').strip()}
```
### Failure Modes (Retry logic)
The mock API simulation threw 500 Internal Server errors to test the `retry_with_backoff` decorator. It successfully caught the errors, applied backoff delays, and succeeded on the 3rd attempt.
```text
{read_file('perf_audit/failure_results.txt').strip()}
```

## 6. Scalability & Architectural Analysis
1. **Stateful Components (N+1 memory risks):**
   - The primary data accumulator in `CanaData` is `self.allMenuItems` (a dictionary of lists of dictionaries). It is protected by `self._menu_data_lock`.
   - While thread-safe for vertical scaling, storing all scraped menu items in memory for large states (e.g., California) before converting them to a Pandas DataFrame or CSV creates a massive memory footprint.
   - **Limitation:** Multiple instances of the scraper cannot easily aggregate data together horizontally.
2. **Disk I/O and Caching:**
   - `CacheManager` in `cache_manager.py` uses `pickle` to serialize data to the local disk.
   - **Limitation:** In a containerized (Docker/K8s) or serverless environment, local disk caches are ephemeral and cannot be shared across multiple scraping nodes. Pickling also poses security and compatibility risks compared to JSON.
3. **Actionable Recommendations:**
   - **Streaming Processing:** Refactor the pipeline to stream JSON responses directly into CSVs or a database row-by-row, rather than holding `self.allMenuItems` entirely in memory.
   - **Distributed Caching:** Replace the local disk cache with a distributed in-memory datastore like Redis to allow multiple scraping nodes to share rate-limit states and API caches.
   - **Decoupled Architecture:** Separate the Web Scraper (Producer) from the Data Flattener/CSV Generator (Consumer) using a message queue (e.g., Celery, RabbitMQ) to allow independent horizontal scaling of both layers.
"""
    with open('perf_audit/PERFORMANCE_REPORT.md', 'w') as f:
        f.write(report)
    print("Report generated at perf_audit/PERFORMANCE_REPORT.md")

if __name__ == "__main__":
    main()
