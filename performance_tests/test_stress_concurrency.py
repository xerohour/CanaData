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


from concurrent_processor import ConcurrentMenuProcessor

def test_stress_locking():
    # Set rate limit to 0 to avoid test timeouts
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    # 10 workers each returning a batch of 100 items
    locations = [{'slug': f'loc_{i}'} for i in range(10)]

    def mock_fetch_and_process(location):
        idx = int(location['slug'].split('_')[1])
        time.sleep(0.001)
        return {
            'listing_id': location['slug'],
            'local_menu_items': [{'id': idx * 100 + j} for j in range(100)],
            'is_empty_menu': False,
            'listing_copy': {},
            'local_extracted_strains': {},
            'menu_items_count': 100
        }

    start_time = time.time()
    processor.process_locations(locations, mock_fetch_and_process)
    duration = time.time() - start_time

    total_items = sum(len(res['local_menu_items']) for res in processor.results.values() if res)
    assert total_items == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
