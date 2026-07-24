import pytest
from CanaData import CanaData
import time

def test_api_rate_limiting(benchmark):
    # Testing concurrent rate limiting overhead
    scraper = CanaData(optimize_processing=True)
    scraper.locations = [{"slug": f"loc{i}", "type": "dispensary"} for i in range(100)]

    def process_mock(*args, **kwargs):
        pass
    scraper._fetch_and_process_menu = process_mock

    def run_concurrent():
        scraper._getMenusConcurrent()

    benchmark(run_concurrent)
