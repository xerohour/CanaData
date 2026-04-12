import pytest
import time
import concurrent.futures
from concurrent_processor import ConcurrentMenuProcessor

def test_high_concurrency_rate_limiter():
    """
    Stress test the ConcurrentMenuProcessor's internal rate limiting lock.
    Verifies that under high thread contention (50 workers, 100 tasks),
    the global lock properly serializes the rate limiting and prevents deadlocks,
    while still completing within a reasonable threshold without hanging indefinitely.
    """
    processor = ConcurrentMenuProcessor(max_workers=50)
    start = time.time()

    def mock_task(i):
        # We only care about testing the lock contention logic here
        processor._wait_for_rate_limit()
        time.sleep(0.01)

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Map ensures we fully iterate over all futures, propagating any exceptions
        list(executor.map(mock_task, range(100)))

    end = time.time()

    # Since 1 request is allowed per second, 100 requests should take roughly 100 seconds
    # Give a small buffer for thread overhead
    duration = end - start
    assert 95 < duration < 120, f"Rate limiting lock failed or deadlocked. Took {duration}s"
