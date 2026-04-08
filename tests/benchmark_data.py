import pytest
import pandas as pd
import json
import time
from optimized_data_processor import OptimizedDataProcessor

def test_benchmark_flattening():
    test_data = []
    for i in range(5000):
        item = {'id': i, 'name': f'Product {i}', 'price': {'amount': 50.0, 'currency': 'USD'}, 'metadata': {'tags': ['a', 'b', 'c'], 'nested': {'deep': {'value': True}}}}
        test_data.append(item)

    all_menu_items = {'loc_1': test_data}
    processor = OptimizedDataProcessor(max_workers=4)

    start_time = time.time()
    processor.process_menu_data(all_menu_items)
    end_time_pandas = time.time() - start_time

    start_time = time.time()
    items_with_location = [dict(item, _location_id=loc_id) for loc_id, items in all_menu_items.items() for item in items]
    [processor._flatten_dictionary_custom(item) for item in items_with_location]
    end_time_custom = time.time() - start_time

    print(f"Pandas processing time: {end_time_pandas:.2f}s")
    print(f"Custom processing time: {end_time_custom:.2f}s")

if __name__ == '__main__':
    test_benchmark_flattening()
