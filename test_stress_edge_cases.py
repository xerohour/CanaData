import pytest
import time
import threading
from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff

def test_concurrent_processor_race_condition():
    # Test if multiple workers accessing shared structures cause race conditions
    locations = [{"slug": f"loc-{i}"} for i in range(1000)]

    # We use a custom process func that simulates mixed latency to cause thread interleaving
    def mixed_latency_process(loc):
        import random
        time.sleep(random.uniform(0.001, 0.01))
        # Deliberately raise exception sometimes to test error list thread safety
        if random.random() < 0.1:
            raise Exception("Simulated Failure")
        return {"id": loc["slug"]}

    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0.0)
    results = processor.process_locations(locations, mixed_latency_process)

    # Assert thread safety of results and errors dict/list
    assert len(processor.results) + len(processor.errors) == 1000

def test_retry_backoff_decorator():
    call_count = 0
    start_time = time.time()

    @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=1.0)
    def flappy_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Flap")
        return "success"

    result = flappy_func()
    end_time = time.time()

    assert result == "success"
    assert call_count == 3
    # First retry: ~0.1s, Second retry: ~0.2s. Total should be > 0.3s
    assert (end_time - start_time) > 0.3
