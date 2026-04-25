import json
import os
import sys

# Ensure root directory is in path for imports to work during CI
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from optimized_data_processor import OptimizedDataProcessor  # noqa: E402
from CanaData import CanaData  # noqa: E402


def test_processing_benchmark_optimized(benchmark):
    sample_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', [])}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0


def test_processing_benchmark_map_reduce(benchmark):
    sample_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])

    def process_data():
        # Simulate map-reduce by directly capturing and returning dictionary
        return {"test-loc": [scraper.flatten_dictionary(item) for item in products]}

    result = benchmark(process_data)
    assert "test-loc" in result


def test_processing_benchmark_legacy(benchmark):
    sample_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])

    def process_data():
        flattened = []
        for item in products:
            flattened.append(scraper.flatten_dictionary(item))
        return flattened

    result = benchmark(process_data)
    assert len(result) > 0
