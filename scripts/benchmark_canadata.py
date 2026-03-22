import os
import time
from unittest.mock import patch
import pytest
from CanaData import CanaData

@pytest.fixture
def mock_canadata_env():
    # Ensure environment limits are off
    os.environ['RATE_LIMIT'] = '0'
    os.environ['MAX_WORKERS'] = '20'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'
    yield
    # Cleanup
    if 'RATE_LIMIT' in os.environ:
        del os.environ['RATE_LIMIT']
    if 'MAX_WORKERS' in os.environ:
        del os.environ['MAX_WORKERS']
    if 'USE_CONCURRENT_PROCESSING' in os.environ:
        del os.environ['USE_CONCURRENT_PROCESSING']


def test_canadata_network_concurrency(benchmark, mock_canadata_env):
    """
    Benchmarks the concurrency of CanaData network requests.
    Simulates network latency using time.sleep within a mock.
    """

    # Generate 50 mock locations to process
    mock_locations = [
        {"slug": f"loc-{i}", "type": "dispensary", "id": f"id-{i}"}
        for i in range(50)
    ]

    # Initialize CanaData instance
    scraper = CanaData(
        max_workers=20,
        rate_limit=0.0,
        cache_enabled=False,
        optimize_processing=False,
        interactive_mode=False
    )
    scraper.locations = mock_locations
    scraper.searchSlug = "test-slug"
    scraper.NonGreenState = False

    def simulated_network_call(*args, **kwargs):
        # Simulate network latency of 50ms
        time.sleep(0.05)
        return {
            "listing": {"id": "1", "slug": "test", "_type": "dispensary"},
            "categories": []
        }

    @patch('CanaData.CanaData.do_request', side_effect=simulated_network_call)
    def run_benchmark(mock_request):
        scraper.getMenus()
        return True

    # Run the benchmark
    _ = benchmark(run_benchmark)
