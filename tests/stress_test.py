import pytest
import os
import sys
import threading
import time
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor

# Stress testing concurrent fetching
@patch('CanaData.CanaData.do_request')
def test_concurrency_failure_modes(mock_do_request):
    """
    Test how `ConcurrentMenuProcessor` and `CanaData` behave under high load
    with rate limits disabled and various simulated failure modes (e.g., 500 errors).
    """
    # Track metrics
    metrics = {
        'success': 0,
        'failure': 0,
        'requests_made': 0
    }
    metrics_lock = threading.Lock()

    def mock_request(url, use_cache=False):
        with metrics_lock:
            metrics['requests_made'] += 1
            count = metrics['requests_made']

        time.sleep(0.005) # simulate latency

        # Simulate an intermittent 500 error every 5th request
        if count % 5 == 0:
            with metrics_lock:
                metrics['failure'] += 1
            return False # emulate a failure in the legacy fallback

        with metrics_lock:
            metrics['success'] += 1

        if 'menu_items' in url:
            return {'data': {'menu_items': [{'id': f'item-{count}', 'name': f'Item {count}'}]}}
        elif 'menu' in url: # legacy fallback
            return {'listing': {'id': str(count), 'slug': f'slug-{count}'}, 'categories': []}
        return {}

    mock_do_request.side_effect = mock_request

    os.environ['RATE_LIMIT'] = '0'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'
    os.environ['MAX_WORKERS'] = '50'

    cana = CanaData(max_workers=50, rate_limit=0)
    cana.searchSlug = 'stress-slug'
    # Setup high concurrency payload
    cana.locations = [{'slug': f'loc-{i}', 'type': 'dispensary'} for i in range(100)]

    start_time = time.time()
    cana.getMenus()
    end_time = time.time()

    elapsed = end_time - start_time

    assert len(cana.locations) == 100
    assert metrics['requests_made'] >= 100 # At least one per location, up to 2 if discovery fails
    # With 50 workers and 0.005s sleep, 100 requests should ideally take very little time
    assert elapsed < 2.0 # Ensure it scaled horizontally
