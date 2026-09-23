import cProfile
import json
import os
import pstats
import sys
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def run_profiling():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if not os.path.exists(sample_file):
        data = {"data": {"products": [{"id": i, "name": f"test_{i}"} for i in range(100)]}}
    else:
        with open(sample_file) as f:
            data = json.load(f)

    # 1. Profile Data Processor
    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 100} # Scale up for profiling

    print("Profiling OptimizedDataProcessor...")
    processor.process_menu_data(menu_items)

    # 2. Profile Concurrent State Update
    print("Profiling Concurrency State Updates...")
    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(worker_id):
        local_items = {}
        for i in range(1000):
            local_items[f"{worker_id}_{i}"] = [{'id': worker_id * 10000 + i, 'name': 'test'}]
        with scraper._menu_data_lock:
            scraper.allMenuItems.update(local_items)

    threads = []
    for i in range(50):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    run_profiling()
    pr.disable()

    with open('profiling_raw_data.prof', 'w') as f:
        ps = pstats.Stats(pr, stream=f)
        ps.sort_stats('cumulative')
        ps.print_stats()

    print("Profiling saved to profiling_raw_data.prof")
