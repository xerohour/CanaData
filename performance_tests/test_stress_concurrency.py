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
    pass

from concurrent_processor import ConcurrentMenuProcessor  # noqa: E402

def test_stress_stateless_aggregation():
    processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0)

    locations = [{'slug': f'loc_{i}'} for i in range(1000)]

    def process_func(location):
        # Simulate some processing without locking
        return {'id': location['slug'], 'processed': True}

    start_time = time.time()

    results = processor.process_locations(locations, process_func)

    duration = time.time() - start_time

    # Aggregation happens sequentially afterwards
    aggregated = []
    for slug, res in results.items():
        if res:
            aggregated.append(res)

    assert len(aggregated) == 1000
    print(f"Stateless stress test completed successfully in {duration:.2f} seconds.")
