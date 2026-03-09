import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from CanaData import CanaData
from concurrent_processor import retry_with_backoff, ConcurrentMenuProcessor

def test_thread_safety_menu_data_lock():
    """Test that CanaData._menu_data_lock prevents race conditions."""
    cana = CanaData()
    cana.allMenuItems = {}
    cana.menuItemsFound = 0
    cana.totalLocations = []

    num_threads = 100
    items_per_thread = 50

    def simulate_menu_processing(thread_id):
        # Create a dummy menu json response
        menu_json = {
            'listing': {'id': f'listing_{thread_id}', 'slug': f'slug_{thread_id}', 'wmid': f'wmid_{thread_id}'},
            'categories': [{'items': [{'id': f'item_{thread_id}_{i}'} for i in range(items_per_thread)]}]
        }
        cana.process_menu_json(menu_json)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(simulate_menu_processing, i) for i in range(num_threads)]
        for future in futures:
            future.result()  # Wait for all to complete

    # Assertions
    assert len(cana.allMenuItems) == num_threads
    assert cana.menuItemsFound == num_threads * items_per_thread
    assert len(cana.totalLocations) == num_threads

def test_retry_with_backoff():
    """Test exponential backoff retries on failure."""
    calls = []

    @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=0.5)
    def flaky_function():
        calls.append(time.time())
        if len(calls) < 3:
            raise ValueError("Simulated network error")
        return "Success"

    start = time.time()
    result = flaky_function()
    end = time.time()

    assert result == "Success"
    assert len(calls) == 3

    # Check delays. First delay ~0.1s, second delay ~0.2s. Total >= 0.3s
    assert end - start >= 0.3

def test_high_concurrency_processor():
    """Test ConcurrentMenuProcessor with a high number of workers."""
    locations = [{'slug': f'loc_{i}', 'type': 'dispensary'} for i in range(50)]

    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0)

    def process_func(location):
        time.sleep(0.01) # Simulate minimal I/O delay
        return True

    start_time = time.time()
    results = processor.process_locations(locations, process_func)
    end_time = time.time()

    assert len(results) == 50
    assert len(processor.errors) == 0
    assert all(results.values())
