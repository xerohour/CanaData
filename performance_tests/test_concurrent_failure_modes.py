import time
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff

def test_retry_with_backoff():
    call_counts = [0]

    @retry_with_backoff(max_retries=3, base_delay=0.01, max_delay=0.1)
    def failing_func():
        call_counts[0] += 1
        if call_counts[0] < 3:
            raise ValueError("Simulated network error")
        return "success"

    result = failing_func()
    assert result == "success"
    assert call_counts[0] == 3

def test_concurrent_processor_failures():
    processor = ConcurrentMenuProcessor(max_workers=5, rate_limit=0.01)
    locations = [{'slug': f'loc_{i}'} for i in range(20)]

    def process_func(location):
        # Simulate random failure
        if int(location['slug'].split('_')[1]) % 5 == 0:
            raise Exception("Simulated processing error")
        time.sleep(0.01)
        return {"status": "ok", "slug": location['slug']}

    _ = processor.process_locations(locations, process_func)

    # Expect 16 successful, 4 failures (0, 5, 10, 15)
    assert len(processor.results) == 16
    assert len(processor.errors) == 4
