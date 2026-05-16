import threading
import time
import os
import sys

# Ensure root directory is in path for imports to work during CI
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from CanaData import CanaData  # noqa: E402


def test_stress_locking():
    from concurrent_processor import ConcurrentMenuProcessor
    locations = [{'slug': f'loc_{i}', 'type': 'dispensary'} for i in range(1000)]

    # We use rate limit 0 to maximize thread pressure during benchmark testing
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    def mock_process(loc):
        return {
            'listing_id': loc['slug'],
            'local_menu_items': [{'id': 'item1'}],
            'is_empty_menu': False,
            'listing_copy': loc,
            'local_extracted_strains': {},
            'menu_items_count': 1
        }

    start_time = time.time()
    results = processor.process_locations(locations, mock_process)
    duration = time.time() - start_time

    assert len(results.keys()) == 1000
    print(f"Concurrent stress test completed successfully in {duration:.2f} seconds.")
