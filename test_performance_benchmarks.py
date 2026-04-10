import pytest
import time
from optimized_data_processor import OptimizedDataProcessor
from concurrent_processor import ConcurrentMenuProcessor
import json
import threading

def load_data():
    try:
        with open('sample_products.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):
                data = [data]
            return {"loc1": data}
    except Exception as e:
        return {"loc1": [{"id": 1, "name": "Test", "nested": {"key": "value"}}]}

def test_optimized_data_processor_benchmark(benchmark):
    data = load_data()
    processor = OptimizedDataProcessor(max_workers=4)

    # Pre-warm
    processor.process_menu_data(data)

    result = benchmark(processor.process_menu_data, data)
    assert result is not None

def mock_process_func(location):
    time.sleep(0.01) # Simulate API call latency
    return {"status": "success"}

def test_concurrent_processor_benchmark(benchmark):
    locations = [{"slug": f"loc-{i}"} for i in range(100)]
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0) # No rate limit for pure concurrency test

    result = benchmark(processor.process_locations, locations, mock_process_func)
    assert len(result) == 100
