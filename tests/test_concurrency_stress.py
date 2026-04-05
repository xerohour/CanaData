import pytest
import time
from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff

def test_concurrent_processor_error_collection():
    processor = ConcurrentMenuProcessor(max_workers=5, rate_limit=0.01)
    locations = [{'slug': f'loc-{i}'} for i in range(20)]

    def failing_process_func(location):
        if int(location['slug'].split('-')[1]) % 2 == 0:
            raise ValueError("Simulated network error")
        return "Success"

    results = processor.process_locations(locations, failing_process_func)

    assert len(results) == 10
    assert len(processor.errors) == 10
    assert processor.errors[0]['error'] == 'Simulated network error'

def test_retry_with_backoff():
    attempts = 0

    @retry_with_backoff(max_retries=3, base_delay=0.01, max_delay=0.1)
    def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception("Temporary failure")
        return "Final success"

    result = flaky_function()
    assert result == "Final success"
    assert attempts == 3
