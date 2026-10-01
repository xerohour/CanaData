import json
import os
import sys
import psutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from optimized_data_processor import OptimizedDataProcessor

def test_memory_usage_large_dataset():
    """Test memory consumption during processing of a very large dataset"""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss

    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if os.path.exists(sample_file):
        with open(sample_file) as f:
            data = json.load(f)
        base_products = data.get('data', {}).get('products', [])
    else:
        # Generate mock data if file not found
        base_products = [{'id': i, 'name': f'mock_product_{i}', 'brand': {'id': 1, 'name': 'mock_brand'}} for i in range(100)]

    # Create large dataset
    menu_items = {'test_dispensary': base_products * 100}

    processor = OptimizedDataProcessor(max_workers=4)
    processor.process_menu_data(menu_items)

    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory

    # Acceptable memory footprint for this amount of data should be reasonable
    # Arbitrary 150MB threshold for this specific large chunk
    assert memory_growth < 150 * 1024 * 1024, f"High memory usage detected: grew by {memory_growth / (1024*1024):.2f} MB"
