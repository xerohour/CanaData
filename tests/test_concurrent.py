import pytest
import time
import concurrent.futures
from concurrent_processor import ConcurrentMenuProcessor

@pytest.fixture
def processor():
    return ConcurrentMenuProcessor(max_workers=5, rate_limit=0.1)

def test_concurrent_processing(processor):
    locations = [{"slug": f"loc-{i}"} for i in range(10)]

    def dummy_process(loc):
        time.sleep(0.05)
        return {"processed": loc["slug"]}

    start_time = time.time()
    results = processor.process_locations(locations, dummy_process)
    end_time = time.time()

    assert len(results) == 10
    # Should be faster than sequential 10 * 0.05 = 0.5s, but rate limited.
    # Rate limit 0.1s/req -> 10 reqs -> 1.0s minimum.
    # Wait, rate limit is per request initiation.

    # If rate limit is 0.1s, and we have 10 items.
    # It should take at least 0.9s (first one is instant).

    assert end_time - start_time >= 0.9

def test_rate_limiting(processor):
    # Test that requests are spaced out
    locations = [{"slug": f"loc-{i}"} for i in range(5)]
    timestamps = []

    def dummy_process(loc):
        timestamps.append(time.time())
        return True

    processor.process_locations(locations, dummy_process)

    timestamps.sort()
    diffs = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]

    # Check that average spacing is close to rate limit
    avg_diff = sum(diffs) / len(diffs)
    assert avg_diff >= 0.09 # Allow some jitter/margin

def test_error_handling(processor):
    locations = [{"slug": "good"}, {"slug": "bad"}]

    def process_with_error(loc):
        if loc["slug"] == "bad":
            raise ValueError("Bad location")
        return "ok"

    results = processor.process_locations(locations, process_with_error)

    assert "good" in results
    assert "bad" not in results
    assert len(processor.errors) == 1
    assert processor.errors[0]["location"]["slug"] == "bad"
