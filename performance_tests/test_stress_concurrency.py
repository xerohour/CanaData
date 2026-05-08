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


def test_stress_concurrent_processor():
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.0)

    locations = [{'id': i, 'slug': f'loc_{i}'} for i in range(1000)]

    def process_func(location):
        time.sleep(0.001)  # Simulate small processing delay
        return {
            'listing_id': location['id'],
            'menu_items': [{'id': location['id']}],
            'listing_copy': location,
            'extracted_strains': {},
            'is_empty': False,
            'count': 1
        }

    start_time = time.time()

    processor.process_locations(locations, process_func)

    duration = time.time() - start_time

    assert len(processor.results) == 1000
    total_count = sum(result['count'] for result in processor.results.values())
    assert total_count == 1000

    print(f"Stress test completed successfully in {duration:.2f} seconds.")
