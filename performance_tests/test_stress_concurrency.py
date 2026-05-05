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
    """Test that ConcurrentMenuProcessor properly aggregates results without locks"""
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    # Create 1000 dummy locations
    locations = [{'slug': f'location-{i}', 'id': f'id-{i}'} for i in range(1000)]

    def process_func(location):
        # Simulate some processing delay
        time.sleep(0.001)
        return {
            'listing_id': location['id'],
            'menu_items': [{'item_id': f"{location['id']}-item-{j}"} for j in range(2)],
            'empty_menu': None,
            'extracted_strains': {},
            'menu_items_count': 2,
            'listing_copy': {'id': location['id'], 'slug': location['slug']}
        }

    start_time = time.time()
    results = processor.process_locations(locations, process_func)
    duration = time.time() - start_time

    assert len(results) == 1000
    assert len(processor.errors) == 0
    print(f"Stress test completed successfully in {duration:.2f} seconds.")
