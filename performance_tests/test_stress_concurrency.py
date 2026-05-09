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


def test_stress_stateless_worker():
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    # Mock locations
    locations = [{'slug': f'loc_{i}', 'id': i} for i in range(1000)]

    # Mock stateless process function
    def process_func(location):
        return {
            'listing_id': location['id'],
            'menu_items': [{'id': location['id']}],
            'is_empty': False,
            'listing_copy': {'slug': location['slug']},
            'extracted_strains': {}
        }

    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)
    start_time = time.time()

    results = processor.process_locations(locations, process_func)

    for slug, result in results.items():
        if result:
            scraper._aggregate_menu_result(result)

    duration = time.time() - start_time
    assert len(scraper.allMenuItems) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
