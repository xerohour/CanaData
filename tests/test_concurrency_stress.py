import time
import pytest
from concurrent_processor import ConcurrentMenuProcessor

def mock_failing_process(location):
    if location['slug'] == 'fail':
        raise Exception("Simulated network failure")
    time.sleep(0.01)
    return {"status": "ok"}

def test_concurrency_high_load_and_failure():
    locations = [{"slug": f"loc{i}"} for i in range(50)]
    locations.append({"slug": "fail"})

    processor = ConcurrentMenuProcessor(max_workers=20, rate_limit=0)
    results = processor.process_locations(locations, mock_failing_process)

    assert len(results) == 50
    assert len(processor.errors) == 1
    assert processor.errors[0]['location']['slug'] == 'fail'
