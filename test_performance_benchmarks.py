import time
from optimized_data_processor import OptimizedDataProcessor
from concurrent_processor import ConcurrentMenuProcessor
import json


def load_data():
    try:
        with open('sample_products.json', 'r') as f:
            data = json.load(f)
            # Make sure it is a list of dicts like a menu item
            items = data.get("data", {}).get("products", [])
            if not items:
                items = [{"id": 1, "name": "Test", "nested": {"key": "value"}}]
            return {"loc1": items}
    except Exception:
        fallback = [{"id": 1, "name": "Test", "nested": {"key": "value"}}]
        return {"loc1": fallback}


def test_optimized_data_processor_benchmark(benchmark):
    data = load_data()

    def process_wrapper():
        # Instantiate inside the benchmark round so state is clean
        processor = OptimizedDataProcessor(max_workers=4)
        return processor.process_menu_data(data)

    result = benchmark(process_wrapper)
    assert result is not None


def mock_process_func(location):
    time.sleep(0.01)  # Simulate API call latency
    return {"status": "success"}


def test_concurrent_processor_benchmark(benchmark):
    locations = [{"slug": f"loc-{i}"} for i in range(100)]

    def process_wrapper():
        # Instantiate inside the benchmark round so state is clean
        processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)
        return processor.process_locations(locations, mock_process_func)

    result = benchmark(process_wrapper)
    assert len(result) == 100
