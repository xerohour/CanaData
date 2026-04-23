import threading
from concurrent_processor import ConcurrentMenuProcessor

def test_concurrent_processing():
    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0)
    locations = [{"slug": f"loc-{i}"} for i in range(100)]
    def dummy_process(loc):
        return {"id": loc["slug"]}
    results = processor.process_locations(locations, dummy_process)
    assert len(results) == 100
    assert len(processor.errors) == 0
