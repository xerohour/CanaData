import time
import threading
from CanaData import CanaData
from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff
from optimized_data_processor import OptimizedDataProcessor

def test_thread_safety():
    """Test thread-safety of CanaData data collections."""
    scraper = CanaData(interactive_mode=False)

    def simulate_processing(listing_id, count):
        menu_json = {
            'listing': {'id': listing_id, 'slug': f'test-{listing_id}', '_type': 'dispensary'},
            'categories': [{'items': [{'name': f'item-{i}'} for i in range(count)]}]
        }
        scraper.process_menu_json(menu_json)

    threads = []
    for i in range(100):
        t = threading.Thread(target=simulate_processing, args=(f'loc-{i}', 10))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(scraper.allMenuItems) == 100
    assert scraper.menuItemsFound == 1000
    assert len(scraper.totalLocations) == 100

def test_concurrency():
    """Benchmark concurrency using ConcurrentMenuProcessor."""
    processor = ConcurrentMenuProcessor(max_workers=5, rate_limit=0.01)
    locations = [{'slug': f'loc-{i}'} for i in range(20)]

    def mock_process(loc):
        time.sleep(0.05) # Simulate IO
        return {'status': 'ok'}

    start_time = time.time()
    results = processor.process_locations(locations, mock_process)
    duration = time.time() - start_time

    assert len(results) == 20
    # 20 items, max_workers=5, 0.05s IO + 0.01s rate limit
    # Should take roughly (20/5) * 0.05 = 0.2s, plus overhead
    assert duration < 2.0

def test_retry_backoff():
    """Test retry backoff mechanism."""
    attempts = []

    @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=1.0)
    def flaky_func():
        attempts.append(time.time())
        if len(attempts) < 3:
            raise Exception("Temporary failure")
        return "Success"

    start_time = time.time()
    result = flaky_func()
    duration = time.time() - start_time

    assert result == "Success"
    assert len(attempts) == 3
    # Delay 1: ~0.1s, Delay 2: ~0.2s => Total delay ~0.3s
    assert duration >= 0.25

def test_data_processing():
    """Benchmark data processing bottlenecks."""
    processor = OptimizedDataProcessor()

    # Generate large synthetic data
    all_menu_items = {}
    for i in range(50):
        items = []
        for j in range(200):
            items.append({
                'name': f'Item {j}',
                'price': {'amount': 10 + j, 'currency': 'USD'},
                'tags': ['indica', 'thc', f'tag-{j}'],
                'metadata': {'nested': {'deep': 'value'}}
            })
        all_menu_items[f'loc-{i}'] = items

    start_time = time.time()
    result = processor.process_menu_data(all_menu_items)
    duration = time.time() - start_time

    assert len(result) == 10000
    assert duration < 5.0 # Processing 10k items should be reasonably fast
