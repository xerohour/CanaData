import pytest
import os
import sys
import json
import pandas as pd
from unittest.mock import patch
import time

# Add parse-script to sys.path to import CanaParse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../parse-script')))
# Add scripts to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor
from CanaParse import CanaParse, FlowerFilter

# 1. Benchmark CanaData Concurrency (Network latency simulation)
@patch('CanaData.CanaData.do_request')
def test_canadata_concurrency(mock_do_request, benchmark):
    # Set up mock network response with latency
    def mock_request(url, use_cache=False):
        time.sleep(0.01) # Simulate 10ms network latency
        if 'menu_items' in url:
            return {'data': {'menu_items': [{'id': '1', 'name': 'Item 1'}]}}
        elif 'menu' in url: # legacy fallback
            return {'listing': {'id': '1', 'slug': 'slug1'}, 'categories': []}
        return {}

    mock_do_request.side_effect = mock_request

    # Configure environment for concurrency testing
    os.environ['RATE_LIMIT'] = '0'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'
    os.environ['MAX_WORKERS'] = '10'

    cana = CanaData(max_workers=10, rate_limit=0)
    cana.searchSlug = 'test-slug'
    # Setup dummy locations
    cana.locations = [{'slug': f'loc-{i}', 'type': 'dispensary'} for i in range(20)]

    def run_concurrency():
        cana.getMenus()

    # Benchmark the concurrent fetching
    _ = benchmark(run_concurrency)


# 2. Benchmark OptimizedDataProcessor Flattening
def test_optimized_processor_flattening(benchmark):
    processor = OptimizedDataProcessor()

    # Create sample nested data mimicking Weedmaps structure
    all_menu_items = {
        f'loc-{i}': [
            {
                'id': f'item-{i}-{j}',
                'name': f'Item {j}',
                'price': {'amount': 10, 'currency': 'USD'},
                'tags': ['indica', 'thc-rich'],
                'strain_data': {'name': 'OG Kush', 'slug': 'og-kush'}
            } for j in range(10)
        ] for i in range(10)
    }

    def run_flattening():
        # process_menu_data calls json_normalize and then _handle_remaining_nesting
        return processor.process_menu_data(all_menu_items)

    _ = benchmark(run_flattening)


# 3. Benchmark CanaParse apply_filters
def test_canaparse_apply_filters(benchmark):
    parser = CanaParse(no_filter=True)

    # Generate mock CSV data (e.g. 1000 rows with 30 columns)
    mock_data = []
    for i in range(1000):
        row = [str(j) for j in range(30)]
        row[11] = str(10.0 + i % 10) # 11 is prices.eighth
        row[20] = 'Flower'           # 20 is category
        row[2] = f'Product {i} THC: 20%' # 2 is name, used in row_str search
        mock_data.append(row)

    parser.raw_data = mock_data

    # Setup a filter
    filter_data = {
        "name": "Test Filter",
        "key": "prices.eighth",
        "compare": "<=",
        "price": 15.0,
        "categories": ["Flower"],
        "thc_floor": 15
    }
    test_filter = FlowerFilter(filter_data)
    parser.filters = [test_filter]

    def run_filters():
        parser.apply_filters()

    _ = benchmark(run_filters)
