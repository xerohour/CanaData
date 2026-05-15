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

from concurrent_processor import ConcurrentMenuProcessor  # noqa: E402
from CanaData import CanaData  # noqa: E402


def test_stress_locking():
    scraper = CanaData(interactive_mode=False)

    # Test stateless concurrency instead of legacy threading
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)
    locations = [{'slug': f'loc_{i}'} for i in range(10)]

    def mock_fetch(location):
        time.sleep(0.001)
        return {
            'listing_id': location['slug'],
            'menu_items': [{'id': f"{location['slug']}_{j}"} for j in range(100)],
            'listing': location,
            'is_empty': False,
            'strains': {},
            'menu_items_count': 100
        }

    start_time = time.time()
    results = processor.process_locations(locations, mock_fetch)

    for result in results.values():
        if result:
            scraper._aggregate_menu_result(result)

    duration = time.time() - start_time

    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
