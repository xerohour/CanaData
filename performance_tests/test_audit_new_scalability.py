import pytest
import concurrent.futures
from CanaData import CanaData

def test_stress_scaling_simulation(benchmark):
    scraper = CanaData()
    scraper.allMenuItems = {}

    # We will simulate high horizontal scale
    def sim_worker(i):
        item = {"id": str(i), "name": f"Scale Item {i}", "prices": {"ounce": [100]}}
        # Simulate network delay for fetching
        with scraper._menu_data_lock:
            if f"loc{i%10}" not in scraper.allMenuItems:
                scraper.allMenuItems[f"loc{i%10}"] = []
            scraper.allMenuItems[f"loc{i%10}"].append(item)

    def run_scale_sim():
        scraper.allMenuItems = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            list(executor.map(sim_worker, range(5000)))

    benchmark(run_scale_sim)
    total_items = sum(len(items) for items in scraper.allMenuItems.values())
    assert total_items == 5000
