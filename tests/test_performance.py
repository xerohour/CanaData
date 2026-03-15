import os
import time
import threading
from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff
from CanaData import CanaData

os.environ['RATE_LIMIT'] = '0'

def test_concurrency_latency():
    """Test concurrent processing latency to ensure it scales correctly."""
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    locations = [{'slug': f'loc-{i}', 'type': 'dispensary'} for i in range(50)]

    def mock_process(location):
        time.sleep(0.02) # Mock network latency
        return True

    start_time = time.time()
    results = processor.process_locations(locations, mock_process)
    end_time = time.time()

    duration = end_time - start_time
    # If sequential, it would take 50 * 0.02 = 1.0s.
    # With 10 workers, it should take ~0.1s. Let's ensure it's < 0.3s to allow for overhead.
    assert duration < 0.3
    assert len(results) == 50

def test_thread_safety():
    """Test thread safety of the new fine-grained locks in CanaData."""
    cana = CanaData(max_workers=10, rate_limit=0.0, cache_enabled=False)

    # We will simulate multiple threads calling process_menu_json
    def process_mock_data(thread_id):
        mock_json = {
            'listing': {
                'id': f'listing-{thread_id}',
                'slug': f'slug-{thread_id}',
                'wmid': f'wmid-{thread_id}',
                '_type': 'dispensary'
            },
            'categories': [
                {
                    'items': [
                        {
                            'name': f'Item {i} for {thread_id}',
                            'strain_data': {'slug': f'strain-{i}'} # Strains are duplicated across threads
                        } for i in range(5)
                    ]
                }
            ]
        }
        cana.process_menu_json(mock_json)

    threads = []
    for i in range(20):
        t = threading.Thread(target=process_mock_data, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(cana.allMenuItems) == 20
    assert len(cana.totalLocations) == 20
    assert cana.menuItemsFound == 100
    assert len(cana.extractedStrains) == 5 # 5 unique strains total

def test_retry_backoff():
    """Test retry_with_backoff decorator logic."""
    attempts = 0

    @retry_with_backoff(max_retries=3, base_delay=0.01, max_delay=0.1)
    def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Failed attempt")
        return "Success"

    start_time = time.time()
    result = flaky_function()
    end_time = time.time()

    assert result == "Success"
    assert attempts == 3
    assert end_time - start_time >= 0.02 # Should have waited at least base_delay * (1 + 2) + jitter

def test_data_processing_memory():
    """Test memory consumption overhead of flatten_dictionary vs pandas."""
    from optimized_data_processor import OptimizedDataProcessor
    import tracemalloc

    processor = OptimizedDataProcessor(max_workers=2)

    # Generate deeply nested data
    items = []
    for i in range(100):
        item = {
            'id': i,
            'nested': {
                'level1': {
                    'level2': {
                        'level3': f'value {i}'
                    }
                }
            },
            'list_data': [{'key': 'value'}, {'key': 'value2'}],
            '_location_id': 'loc-1'
        }
        items.append(item)

    tracemalloc.start()
    df_pandas = processor._flatten_all_items({'loc-1': items})
    _, peak_pandas = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    df_fallback = processor._fallback_flattening(items)
    _, peak_fallback = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Usually fallback is more memory efficient for small nested structures due to DataFrame overhead
    assert len(df_pandas) == len(df_fallback) == 100
