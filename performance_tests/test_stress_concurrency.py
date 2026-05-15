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

def test_stress_concurrency():
    scraper = CanaData(interactive_mode=False)
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    locations = [{'slug': f'loc_{i}'} for i in range(100)]

    def mock_process_func(location):
        time.sleep(0.001)
        return {
            'listing_id': location['slug'],
            'local_menu_items': [{'id': f"{location['slug']}_{j}"} for j in range(10)],
            'is_empty_menu': False,
            'listing_copy': {'slug': location['slug']},
            'local_extracted_strains': {},
            'menu_items_count': 10
        }

    start_time = time.time()
    processor.process_locations(locations, mock_process_func)

    for _, result in processor.results.items():
        if result:
            scraper._aggregate_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 100
    assert scraper.menuItemsFound == 1000
    assert len(scraper.totalLocations) == 100
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
