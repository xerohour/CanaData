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
from concurrent_processor import ConcurrentMenuProcessor  # noqa: E402


def test_stress_concurrency():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def process_mock_location(location):
        time.sleep(0.001)  # Simulate I/O
        return {
            'listing_id': location['id'],
            'local_menu_items': [{'id': f"{location['id']}_{j}"} for j in range(100)],
            'is_empty_menu': False,
            'listing_copy': location,
            'local_extracted_strains': {},
            'menu_items_count': 100
        }

    locations = [{'id': f'loc_{i}', 'slug': f'loc-slug-{i}'} for i in range(10)]

    # Use 0.0 rate limit for fast testing
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    start_time = time.time()

    results = processor.process_locations(locations, process_mock_location)

    for slug, result in results.items():
        if result:
            scraper._aggregate_menu_result(result)

    duration = time.time() - start_time

    assert len(scraper.allMenuItems) == 10
    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
