import pytest
import time
import os
import logging
from unittest.mock import patch, MagicMock
from CanaData import CanaData
import threading

logger = logging.getLogger(__name__)

def test_thread_safety(benchmark):
    """
    Test thread safety of CanaData data collections when processing many locations concurrently.
    We mock the network request to simulate a network delay and ensure parallel workers
    are successfully pushing to the same dictionaries/lists without losing data.
    """
    os.environ['RATE_LIMIT'] = '0'
    os.environ['MAX_WORKERS'] = '20'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'

    # We will simulate 100 locations
    num_locations = 100
    mock_locations = [{'id': str(i), 'slug': f'loc-{i}', 'type': 'dispensary'} for i in range(num_locations)]

    # Each location has 10 menu items
    num_items_per_loc = 10

    def simulate_do_request(url, use_cache=True):
        time.sleep(0.01) # Simulate network latency 10ms

        # If it's a discovery menu_items url
        if 'menu_items' in url:
            items = [{'id': f'item-{i}', 'name': f'Item {i}', 'price': {'amount': 10}} for i in range(num_items_per_loc)]
            return {'data': {'menu_items': items}, 'meta': {'total_menu_items': num_items_per_loc}}
        return None

    def run_concurrent_process():
        cana = CanaData(interactive_mode=False)
        cana.locations = mock_locations
        cana.NonGreenState = False

        with patch.object(cana, 'do_request', side_effect=simulate_do_request):
            cana.getMenus()

        return cana

    cana = benchmark(run_concurrent_process)

    assert cana.menuItemsFound == num_locations * num_items_per_loc
    assert len(cana.allMenuItems) == num_locations

def test_flatten_performance(benchmark):
    """Benchmark the custom vs optimized flattening."""
    cana = CanaData(optimize_processing=False, interactive_mode=False)

    # Generate large fake nested payload
    payload = {
        'id': '123',
        'product': {
            'name': 'Test',
            'brand': {'name': 'BrandX', 'id': '456'},
            'variants': [
                {'price': 10, 'weight': '1g'},
                {'price': 20, 'weight': '3.5g'}
            ],
            'deep': {'nested': {'property': 'value'}}
        }
    }

    def run_flatten():
        for _ in range(1000):
            _ = cana.flatten_dictionary(payload)

    benchmark(run_flatten)
