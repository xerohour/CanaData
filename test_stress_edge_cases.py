import time
from concurrent_processor import ConcurrentMenuProcessor, retry_with_backoff


def test_concurrent_processor_race_condition():
    # Test if multiple workers accessing shared structures
    locations = [{"slug": f"loc-{i}"} for i in range(1000)]

    def mixed_latency_process(loc):
        import random
        time.sleep(random.uniform(0.001, 0.01))
        # Deliberately raise exception sometimes to test error
        if random.random() < 0.1:
            raise ValueError("Simulated Failure")
        return {"id": loc["slug"]}

    processor = ConcurrentMenuProcessor(max_workers=50, rate_limit=0.0)
    _ = processor.process_locations(locations, mixed_latency_process)

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
    # The backoff is calculated as:
    # min(base_delay * (2 ** (retries - 1)), max_delay) + jitter
    # Retry 1: min(0.1 * 2^0, 1.0) = 0.1 + jitter (0 to 0.01)
    # Retry 2: min(0.1 * 2^1, 1.0) = 0.2 + jitter (0 to 0.02)
    # Total time > 0.25 considering minimums and negligible jitter.
    assert (end_time - start_time) > 0.25
