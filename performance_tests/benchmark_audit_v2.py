import json
import os
import pytest

from optimized_data_processor import OptimizedDataProcessor
from cache_manager import CacheManager

def load_sample_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'sample_products.json')
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return {"loc_1": data['data']['products']}
    except FileNotFoundError:
        return {"loc_1": [{"id": i, "name": f"Product {i}", "price": i*10} for i in range(100)]}

@pytest.fixture(scope="module")
def sample_data():
    return load_sample_data()

def test_benchmark_data_processing_v2(benchmark, sample_data):
    processor = OptimizedDataProcessor()

    def run_process():
        return processor.process_menu_data(sample_data)

    result = benchmark(run_process)
    assert result is not None

def test_benchmark_cache_manager_v2(benchmark):
    cache = CacheManager(enable_disk_cache=False)

    def run_cache():
        for i in range(1000):
            cache.set(f"url_{i}", {"data": i})
        for i in range(1000):
            cache.get(f"url_{i}")

    benchmark(run_cache)
