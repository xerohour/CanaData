import pytest
import time
import threading
from unittest.mock import patch, MagicMock
from CanaData import CanaData
from concurrent_processor import retry_with_backoff

@pytest.fixture
def cana():
    cana_instance = CanaData(max_workers=5, interactive_mode=False)
    # Configure required lists to prevent NoneType errors in loops
    cana_instance.locations = []
    cana_instance.searchSlug = "test_slug"
    return cana_instance


def test_thread_safety(cana):
    """Test thread-safety of CanaData with concurrent menu processing using fine-grained locks."""
    # Setup test mock data
    num_threads = 50
    items_per_thread = 10

    def simulate_menu_processing(listing_id):
        # Create mock menu json with unique item data
        mock_menu = {
            "listing": {
                "id": listing_id,
                "slug": f"test-dispensary-{listing_id}",
                "wmid": listing_id * 10
            },
            "categories": [
                {
                    "title": "Flower",
                    "items": [
                        {
                            "name": f"Item {i}",
                            "strain_data": {
                                "slug": f"strain-{listing_id}-{i}",
                                "name": f"Strain {listing_id}-{i}",
                            },
                            "id": listing_id * 100 + i
                        } for i in range(items_per_thread)
                    ]
                }
            ]
        }
        cana.process_menu_json(mock_menu)

    # Execute concurrent processing
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=simulate_menu_processing, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Verify counts and thread safety
    assert cana.menuItemsFound == num_threads * items_per_thread
    assert len(cana.totalLocations) == num_threads
    assert len(cana.allMenuItems) == num_threads
    assert len(cana.extractedStrains) == num_threads * items_per_thread

@patch('CanaData.CanaData.do_request')
def test_concurrency_latency(mock_do_request, cana):
    """Test concurrency latency by mocking network delay to isolate application logic."""
    num_locations = 10
    mock_delay = 0.1 # Simulate 100ms network latency

    # Mock return values and add simulated latency
    def delayed_response(*args, **kwargs):
        time.sleep(mock_delay)
        return {"data": {"menu_items": []}, "meta": {"total_menu_items": 0}}

    mock_do_request.side_effect = delayed_response

    # Setup mock locations
    cana.locations = [
        {"slug": f"loc-{i}", "type": "dispensary", "id": i}
        for i in range(num_locations)
    ]

    # Enable concurrent processing
    import os
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'
    os.environ['MAX_WORKERS'] = '10'
    os.environ['RATE_LIMIT'] = '0' # Disable rate limiter for testing parallel latency

    start_time = time.time()
    cana.getMenus()
    duration = time.time() - start_time

    # Ensure parallel execution: Total duration should be much less than sequential execution
    # Sequential would be: 10 * 0.1 = 1.0s.
    # Concurrent with 10 workers should be close to 0.1s
    assert duration < (num_locations * mock_delay) * 0.8
    assert mock_do_request.call_count >= num_locations

def test_retry_backoff():
    """Test exponential backoff logic for retrying requests."""

    mock_func = MagicMock(side_effect=[Exception("Network Error"), Exception("Network Error"), "Success"])

    # Track execution times to measure backoff
    start_time = time.time()

    @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=1.0)
    def resilient_call():
        return mock_func()

    result = resilient_call()
    duration = time.time() - start_time

    assert result == "Success"
    assert mock_func.call_count == 3
    # First retry waits 0.1s, second retry waits ~0.2s.
    # Total duration should be at least 0.3s
    assert duration >= 0.3
