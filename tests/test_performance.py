"""
Performance and scalability tests for CanaData.

These tests verify that concurrent processing is faster than sequential,
that the cache provides measurable benefit, and that data processing
scales reasonably with dataset size.
"""

import time
import pytest

from concurrent_processor import ConcurrentMenuProcessor
from optimized_data_processor import OptimizedDataProcessor


class TestConcurrencyPerformance:
    """Benchmark concurrent vs sequential processing."""

    def test_concurrent_faster_than_sequential(self, concurrent_processor):
        """Concurrent processing should beat sequential for I/O-bound work."""
        locations = [{"slug": f"loc-{i}", "type": "dispensary"} for i in range(10)]

        def slow_process(loc):
            time.sleep(0.05)
            return {"items": [loc["slug"]]}

        # Sequential baseline
        start = time.time()
        for loc in locations:
            slow_process(loc)
        sequential_time = time.time() - start

        # Concurrent run
        start = time.time()
        results = concurrent_processor.process_locations(locations, slow_process)
        concurrent_time = time.time() - start

        assert len(results) == 10
        # With 3 workers and 0.05s per task, concurrent should be significantly faster
        assert concurrent_time < sequential_time, (
            f"concurrent ({concurrent_time:.2f}s) should be faster than "
            f"sequential ({sequential_time:.2f}s)"
        )


class TestCachePerformance:
    """Verify caching provides measurable speed improvement."""

    def test_cache_faster_than_repeated_work(self, cache_manager):
        """Lookups from cache should be cheaper than simulated API calls."""
        iterations = 50

        # Simulate work without cache
        start = time.time()
        for i in range(iterations):
            time.sleep(0.005)
        no_cache_time = time.time() - start

        # Prime cache then read from it
        for i in range(iterations):
            cache_manager.set(f"http://api.test/{i}", {"v": i})

        start = time.time()
        for i in range(iterations):
            cache_manager.get(f"http://api.test/{i}")
        cache_time = time.time() - start

        assert cache_time < no_cache_time, (
            f"cache reads ({cache_time:.3f}s) should be faster than "
            f"simulated API ({no_cache_time:.3f}s)"
        )


class TestDataProcessingScalability:
    """Verify data processing scales reasonably with input size."""

    @pytest.mark.parametrize("num_items", [100, 500, 1000])
    def test_processing_scales(self, optimized_processor, num_items):
        """Processing N items should complete in reasonable time."""
        items_per_loc = max(1, num_items // 10)
        data = {
            f"loc-{i}": [
                {"name": f"Product-{j}", "price": {"amount": j, "currency": "USD"}}
                for j in range(items_per_loc)
            ]
            for i in range(10)
        }

        start = time.time()
        result = optimized_processor.process_menu_data(data)
        elapsed = time.time() - start

        assert len(result) == items_per_loc * 10
        # Should complete well under 10 seconds even for 1000 items
        assert elapsed < 10, f"Processing {num_items} items took {elapsed:.2f}s"

    def test_large_dataset_memory_safe(self, optimized_processor):
        """Processing a large dataset should not crash."""
        data = {
            f"loc-{i}": [
                {
                    "name": f"P-{j}",
                    "price": {"amount": j, "currency": "USD"},
                    "attrs": {f"a{k}": k for k in range(5)},
                }
                for j in range(50)
            ]
            for i in range(20)
        }

        result = optimized_processor.process_menu_data(data)
        assert len(result) == 1000
