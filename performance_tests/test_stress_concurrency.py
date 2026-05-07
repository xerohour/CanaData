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

from concurrent_processor import ConcurrentMenuProcessor  # noqa: E402


def test_stress_concurrency():
    # Instantiate ConcurrentMenuProcessor with rate_limit=0.0 to prevent timeouts
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    # We will simulate processing 1000 locations
    locations = [{'slug': f'loc_{i}'} for i in range(1000)]

    def mock_process_location(location):
        # Simulate some work
        time.sleep(0.001)
        # Return mocked data struct:
        # (listing_id, local_menu_items, empty_menu, strains_dict, menu_items_count, locations_list)
        return (
            location['slug'],
            [{'id': f"{location['slug']}_item"}],
            {},
            {},
            1,
            [{'slug': location['slug']}]
        )

    start_time = time.time()
    processor.process_locations(locations, mock_process_location)

    # Simulate the main thread aggregation that happens in _getMenusConcurrent
    all_menu_items = {}
    for result in processor.results.values():
        if result:
            listing_id, local_menu_items, empty_menu, strains_dict, menu_items_count, locations_list = result
            all_menu_items[listing_id] = local_menu_items

    duration = time.time() - start_time

    assert len(all_menu_items) == 1000
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
