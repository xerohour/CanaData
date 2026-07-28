import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from concurrent_processor import ConcurrentMenuProcessor

def test_simulate_n_plus_one_fetching(benchmark):
    # Simulates N+1 querying: sequential fetching of N locations
    def fetch_sequential():
        locations = [{'slug': f'loc_{i}'} for i in range(50)]
        results = {}
        for loc in locations:
            # mock processing time
            results[loc['slug']] = {'menu_items': [{'id': 1}]}
        return len(results)

    result = benchmark(fetch_sequential)
    assert result == 50

def test_simulate_concurrent_fetching(benchmark):
    # Simulates batched/concurrent fetching avoiding N+1
    def fetch_concurrent():
        locations = [{'slug': f'loc_{i}'} for i in range(50)]
        processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0)

        def process_func(loc):
            return {'menu_items': [{'id': 1}]}

        results = processor.process_locations(locations, process_func)
        return len(results)

    result = benchmark(fetch_concurrent)
    assert result == 50
