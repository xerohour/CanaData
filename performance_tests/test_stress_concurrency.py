from concurrent_processor import ConcurrentMenuProcessor
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


def test_stress_concurrency_stateless():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    locations = [{'slug': f'loc-{i}', 'id': f'id-{i}'} for i in range(100)]

    def mock_process_location(location):
        items = [{'id': f"item-{location['slug']}-{j}"} for j in range(10)]
        time.sleep(0.001)  # Simulate some work
        return {
            'allMenuItems': {location['id']: items},
            'menuItemsFound': 10
        }

    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    start_time = time.time()
    results = processor.process_locations(locations, mock_process_location)

    for result in results.values():
        scraper._merge_menu_results(result)

    duration = time.time() - start_time

    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 1000
    assert scraper.menuItemsFound == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
