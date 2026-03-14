import os
import time
import threading
from unittest.mock import patch
from CanaData import CanaData
from concurrent_processor import retry_with_backoff

class TestPerformance:
    def test_thread_safety(self):
        """Test that fine-grained locks correctly handle concurrent updates."""
        cana = CanaData(max_workers=5, optimize_processing=False, cache_enabled=False)

        # We need to simulate multiple threads calling process_menu_json
        def worker(listing_id, count):
            menu_json = {
                'listing': {
                    'id': listing_id,
                    'slug': f'slug-{listing_id}',
                    'wmid': listing_id
                },
                'categories': [
                    {
                        'items': [{'name': f'item-{i}'} for i in range(count)]
                    }
                ]
            }
            cana.process_menu_json(menu_json)

        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(f'listing-{i}', 5))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert cana.menuItemsFound == 50
        assert len(cana.allMenuItems) == 10
        assert len(cana.totalLocations) == 10

    @patch('CanaData.CanaData.do_request')
    def test_concurrency_latency(self, mock_do_request):
        """Test performance of concurrent processing with mocked network latency."""
        # Disable environment rate limiting
        os.environ['RATE_LIMIT'] = '0'
        os.environ['USE_CONCURRENT_PROCESSING'] = 'true'

        # Simulate network latency
        def slow_request(*args, **kwargs):
            time.sleep(0.1)
            # Return empty response to skip detailed processing in this test
            return {'data': {'listings': []}}

        mock_do_request.side_effect = slow_request

        cana = CanaData(max_workers=10, rate_limit=0.0, cache_enabled=False, optimize_processing=False)

        # Mock some locations
        for i in range(20):
            cana.locations.append({
                'id': f'id-{i}',
                'slug': f'slug-{i}',
                'type': 'dispensary'
            })

        start_time = time.time()
        cana.getMenus()
        end_time = time.time()

        duration = end_time - start_time

        # With 20 items and 10 workers, it should take ~2 cycles of 0.1s each, so around 0.2s total
        # rather than 2.0s if it were purely sequential. We allow some overhead.
        assert duration < 1.0, f"Concurrent processing took too long: {duration}s"

    def test_retry_backoff(self):
        """Test that the retry backoff logic correctly handles failures and eventual success."""

        class TestException(Exception):
            pass

        attempts = []

        @retry_with_backoff(max_retries=3, base_delay=0.01, max_delay=0.1)
        def unstable_function():
            attempts.append(time.time())
            if len(attempts) < 3:
                raise TestException("Failed")
            return "Success"

        result = unstable_function()

        assert result == "Success"
        assert len(attempts) == 3

        # Verify there was a delay between attempts
        assert attempts[1] - attempts[0] >= 0.01
        assert attempts[2] - attempts[1] >= 0.01
