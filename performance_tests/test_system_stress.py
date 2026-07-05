import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from concurrent_processor import ConcurrentMenuProcessor

def test_concurrent_processor_rate_limit(benchmark):
    def run_stress():
        processor = ConcurrentMenuProcessor(max_workers=10, rate_limit=0.01)
        locations = [{'slug': f'loc-{i}'} for i in range(50)]

        def dummy_process(loc):
            time.sleep(0.001)
            return loc['slug']

        results = processor.process_locations(locations, dummy_process)
        return len(results)

    result = benchmark(run_stress)
    assert result == 50
