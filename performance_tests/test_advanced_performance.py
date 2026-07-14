import os
import sys
import json
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor

def test_large_nesting_performance(benchmark):
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor()

    # We will simulate the input format `all_menu_items` (Dict[str, List[Dict]])
    products = data.get('data', {}).get('products', [])
    all_menu_items = {str(uuid.uuid4()): products for _ in range(50)}

    def process_data():
        return processor.process_menu_data(all_menu_items)

    result = benchmark(process_data)
    assert len(result) > 0
