import concurrent.futures

from CanaData import CanaData


def test_stress_high_concurrency(benchmark):
    scraper = CanaData()
    scraper.allMenuItems = {}
    def worker_task(i):
        item = {"id": str(i), "name": f"Item {i}", "prices": {"ounce": [100]}}
        with scraper._menu_data_lock:
            if "loc1" not in scraper.allMenuItems:
                scraper.allMenuItems["loc1"] = []
            scraper.allMenuItems["loc1"].append(item)
    def run_stress():
        scraper.allMenuItems = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            list(executor.map(worker_task, range(2000)))
    benchmark(run_stress)
    assert len(scraper.allMenuItems["loc1"]) == 2000
