import json
from optimized_data_processor import OptimizedDataProcessor
from CanaData import CanaData

def test_processing_benchmark_optimized(benchmark):
    with open("sample_products.json") as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', [])}

    def process_data():
        return processor.process_menu_data(menu_items)

    result = benchmark(process_data)
    assert len(result) > 0

def test_processing_benchmark_legacy(benchmark):
    with open("sample_products.json") as f:
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
