import gc
import os

import psutil

from CanaData import CanaData


def test_memory_leak_scraping():
    process = psutil.Process(os.getpid())
    gc.collect()
    start_memory = process.memory_info().rss

    scraper = CanaData(optimize_processing=True)
    scraper.allMenuItems = {
        "loc1": [{"id": str(i), "name": f"Item {i}", "nested": {"val": i}} for i in range(50000)]
    }
    scraper.organize_into_clean_list()

    gc.collect()
    end_memory = process.memory_info().rss

    # Assert memory doesn't explode (e.g. less than 200MB growth for 50k items)
    assert (end_memory - start_memory) < 200 * 1024 * 1024

def test_api_failure_modes(benchmark):
    scraper = CanaData(optimize_processing=True)
    scraper.locations = [{"slug": "loc1", "type": "dispensary"}]
    scraper.max_workers = 5
    scraper.rate_limit = 0

    # Simulate API failure
    def mock_fetch(location):
        raise ConnectionError("Simulated API failure")

    scraper._fetch_and_process_menu = mock_fetch

    def run_concurrent():
        try:
            scraper._getMenusConcurrent()
        except Exception:
            pass

    benchmark(run_concurrent)
