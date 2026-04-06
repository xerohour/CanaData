import pytest
import time
from concurrent_processor import ConcurrentMenuProcessor

# Mock locations and processor function
def mock_locations(num_locations=20):
    return [{"slug": f"location-{i}", "type": "dispensary"} for i in range(num_locations)]

def mock_process_func_fast(location):
    # Simulate very fast local fetch (e.g. cache hit)
    time.sleep(0.01)
    return {"status": "ok", "items": 100}

def mock_process_func_slow(location):
    # Simulate network latency
    time.sleep(0.5)
    return {"status": "ok", "items": 100}

def mock_process_func_error(location):
    if int(location['slug'].split('-')[1]) % 5 == 0:
        raise ValueError("Network timeout")
    time.sleep(0.1)
    return {"status": "ok", "items": 100}

# --- Benchmarks ---

def test_benchmark_fast_processing(benchmark):
    locations = mock_locations(50)
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0) # rate limit 0 for max throughput

    def run_processor():
        processor.process_locations(locations, mock_process_func_fast)
        return processor.results

    result = benchmark(run_processor)
    assert len(result) == 50

def test_benchmark_rate_limiting(benchmark):
    locations = mock_locations(10)
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.1) # 100ms rate limit

    def run_processor():
        processor.process_locations(locations, mock_process_func_fast)
        return processor.results

    # Should take at least 1.0 seconds total due to rate limit lock, despite workers
    result = benchmark.pedantic(run_processor, iterations=1, rounds=3)
    assert len(result) == 10

def test_benchmark_error_handling(benchmark):
    locations = mock_locations(50)
    processor = ConcurrentMenuProcessor(max_workers=5, rate_limit=0.0)

    def run_processor():
        processor.process_locations(locations, mock_process_func_error)
        return processor.errors

    result = benchmark.pedantic(run_processor, iterations=1, rounds=3)
    # Every 5th item errors -> 10 errors
    assert len(processor.errors) == 10
