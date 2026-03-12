import time
import threading
from unittest.mock import patch
from concurrent_processor import ConcurrentMenuProcessor
from cache_manager import CacheManager
from CanaData import CanaData

class TestPerformance:
    """Performance and benchmarking tests"""

    @patch('CanaData.CanaData.do_request')
    def test_concurrent_vs_sequential_processing(self, mock_do_request):
        """Benchmark concurrent vs sequential processing using real CanaData class"""
        # Create a CanaData instance
        cana_seq = CanaData()
        cana_conc = CanaData()
        cana_conc.max_workers = 10
        cana_conc.rate_limit = 0 # no rate limit for test

        # Fake locations
        locations = [{"slug": f"test-{i}", "type": "dispensary"} for i in range(20)]
        cana_seq.locations = locations
        cana_conc.locations = locations

        # We need to simulate a network request that takes some time,
        # but returns a valid JSON that process_menu_json can parse (or fail gracefully).
        # We will mock `_fetch_and_process_menu` to avoid deep mocking of requests
        # and just focus on the concurrent processor overhead vs sequential.
        def mock_fetch_and_process(location):
            time.sleep(0.05)
            return {"items": [f"item-{location['slug']}"]}

        with patch.object(CanaData, '_fetch_and_process_menu', side_effect=mock_fetch_and_process):
            # 1. Test Sequential Execution
            start_time = time.time()
            cana_seq._getMenusSequential()
            seq_duration = time.time() - start_time

            # 2. Test Concurrent Execution
            start_time = time.time()
            cana_conc._getMenusConcurrent()
            conc_duration = time.time() - start_time

            # Verify concurrent is faster
            assert conc_duration < seq_duration
            assert conc_duration < (seq_duration / 2)

    def test_thread_safety(self):
        """Test thread safety under high concurrency using ConcurrentMenuProcessor"""
        locations = [{"slug": f"loc-{i}"} for i in range(100)]
        processor = ConcurrentMenuProcessor(max_workers=20, rate_limit=0)

        shared_resource = []
        resource_lock = threading.Lock()

        def process_with_mutation(location):
            # Mutate shared state
            with resource_lock:
                shared_resource.append(location['slug'])
            return {"slug": location['slug']}

        results = processor.process_locations(locations, process_with_mutation)

        # Verify no data was lost to race conditions
        assert len(shared_resource) == 100
        assert len(results) == 100

    def test_cache_performance_benefit(self):
        """Test performance benefit of caching using CacheManager"""
        cache = CacheManager(cache_dir="test_perf_cache", enable_disk_cache=False)
        url = "https://api.example.com/data"
        data = {"big": "payload" * 1000}

        # Simulate initial slow request
        def slow_fetch():
            time.sleep(0.2)
            cache.set(url, data)
            return data

        # 1. Uncached fetch
        start_time = time.time()
        res1 = slow_fetch()
        uncached_duration = time.time() - start_time

        # 2. Cached fetch
        start_time = time.time()
        res2 = cache.get(url)
        cached_duration = time.time() - start_time

        assert res1 == res2
        assert cached_duration < uncached_duration
        assert cached_duration < 0.01  # Should be near instantaneous

    def test_retry_backoff_performance(self):
        """Test that exponential backoff correctly delays requests"""
        from concurrent_processor import retry_with_backoff

        attempts = 0

        @retry_with_backoff(max_retries=3, base_delay=0.1, max_delay=0.5)
        def failing_func():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise Exception("Network Error")
            return "Success"

        start_time = time.time()
        res = failing_func()
        duration = time.time() - start_time

        assert res == "Success"
        assert attempts == 3
        # Attempt 1 fails -> sleep(0.1 + jitter)
        # Attempt 2 fails -> sleep(0.2 + jitter)
        # Attempt 3 succeeds
        # Total delay should be at least 0.3s
        assert duration >= 0.3
