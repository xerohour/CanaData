import time
import os
from unittest.mock import patch
from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff
from CanaData import CanaData

# --- Retry Logic Backoff Benchmark & Test ---

def test_retry_with_backoff():
    # We will simulate a function that fails twice, then succeeds
    call_times = []

    @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=1.0)
    def flaky_function():
        call_times.append(time.time())
        if len(call_times) < 3:
            raise ValueError("Failed!")
        return "Success!"

    start_time = time.time()
    result = flaky_function()
    end_time = time.time()

    assert result == "Success!"
    assert len(call_times) == 3

    # Check delays
    delay1 = call_times[1] - call_times[0]
    delay2 = call_times[2] - call_times[1]

    # base_delay=0.1, max_retries=3
    # Retry 1: delay = 0.1 * (2**0) = 0.1s (+ jitter)
    # Retry 2: delay = 0.1 * (2**1) = 0.2s (+ jitter)
    assert delay1 >= 0.1
    assert delay2 >= 0.2

# --- ConcurrentMenuProcessor Success & Throughput Test ---

def mock_process_success(location):
    time.sleep(0.01) # Simulate some processing
    return {"status": "ok", "slug": location['slug']}

def test_concurrent_processor_success():
    processor = ConcurrentMenuProcessor(max_workers=5, rate_limit=0)
    locations = [{"slug": f"loc-{i}"} for i in range(20)]

    start_time = time.time()
    results = processor.process_locations(locations, mock_process_success)
    end_time = time.time()

    assert len(results) == 20
    assert len(processor.errors) == 0
    # With 5 workers, 20 items taking 0.01s each should take around 0.04s, but definitely less than 0.2s (sequential time)
    assert (end_time - start_time) < 0.2

# --- ConcurrentMenuProcessor Rate Limit Test ---

def test_concurrent_processor_rate_limit():
    # Rate limit of 0.1s between tasks
    processor = ConcurrentMenuProcessor(max_workers=5, rate_limit=0.1)
    locations = [{"slug": f"loc-{i}"} for i in range(5)]

    start_time = time.time()
    results = processor.process_locations(locations, mock_process_success)
    end_time = time.time()

    assert len(results) == 5
    # 5 tasks with 0.1s rate limit should take at least 0.4s
    # The first task starts at 0, second at 0.1, third at 0.2, fourth at 0.3, fifth at 0.4
    assert (end_time - start_time) >= 0.4

# --- Thread Safety / Race Conditions in Distributed System Mocks ---

def test_concurrent_processor_thread_safety():
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0)
    locations = [{"slug": f"loc-{i}"} for i in range(100)]

    shared_counter = 0
    # Deliberately use a non-thread-safe counter increment to see if our wrapper handles execution properly
    # Actually, we test if process_locations itself safely returns results without dropping any.

    def process_func(location):
        nonlocal shared_counter
        # We don't guarantee thread safety of process_func itself here,
        # but we guarantee that ConcurrentMenuProcessor captures all results
        # without losing any items from the dictionary
        return location['slug']

    results = processor.process_locations(locations, process_func)

    assert len(results) == 100
    assert len(processor.errors) == 0

    # Verify all slugs are present
    for i in range(100):
        assert f"loc-{i}" in results

# --- CanaData High-Concurrency & Mocking Network Layer ---

def mock_do_request(self, url, use_cache=True):
    # Simulate network latency
    time.sleep(0.02)

    if "menu_items" in url:
        return {
            "meta": {"total_menu_items": 10},
            "data": {"menu_items": [{"id": f"item-{i}", "name": "Test"} for i in range(10)]}
        }
    return None

@patch('CanaData.CanaData.do_request', new=mock_do_request)
def test_canadata_concurrency():
    # Ensure rate limit is disabled for concurrency test
    os.environ['RATE_LIMIT'] = '0'
    os.environ['MAX_WORKERS'] = '10'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'

    cana = CanaData(max_workers=10, rate_limit=0, cache_enabled=False, optimize_processing=True, interactive_mode=False)
    cana.searchSlug = "test-concurrency"
    cana.locations = [{"id": str(i), "slug": f"loc-{i}", "type": "dispensary", "wmid": f"wmid-{i}", "name": f"Loc {i}"} for i in range(50)]

    start_time = time.time()
    cana.getMenus()
    end_time = time.time()

    # Verify thread safety of allMenuItems and menuItemsFound
    assert len(cana.allMenuItems) == 50
    assert cana.menuItemsFound == 500  # 50 locations * 10 items

    # 50 requests taking 0.02s each with 10 workers should take roughly ~0.1s + overhead.
    # Sequentially it would take > 1.0s.
    assert (end_time - start_time) < 0.5
