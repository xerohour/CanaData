import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor
from CanaData import CanaData

def test_benchmark_throughput_large_workload(benchmark):
    """Benchmark high-throughput dictionary flattening on a large simulated payload."""
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', []) * 10 # Artificially large workload

    def process_data():
        flattened = []
        for item in products:
            flattened.append(scraper.flatten_dictionary(item))
        return flattened

    result = benchmark(process_data)
    assert len(result) > 0

def test_benchmark_optimized_processor_scaling(benchmark):
    """Benchmark the new pandas processor on large batch chunks."""
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    products = data.get('data', {}).get('products', []) * 10
    menu_items = {'test_dispensary': products}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0
