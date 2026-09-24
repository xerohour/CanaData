from memory_profiler import profile
from CanaData import CanaData
import time

@profile
def test_memory_leak():
    scraper = CanaData(cache_enabled=False, optimize_processing=True, max_workers=5)
    for _ in range(5):
        for i in range(1000):
            with scraper._menu_data_lock:
                item = {"id": i, "name": f"Item {i}", "desc": "A long description to take up some memory"}
                flattened = scraper.flatten_dictionary(item)
                scraper.allMenuItems[f"batch_{_}_{i}"] = [flattened]
        time.sleep(0.1)

if __name__ == "__main__":
    test_memory_leak()
