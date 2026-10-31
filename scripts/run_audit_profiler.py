import cProfile
import pstats
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def profile_codebase():
    print("Generating codebase profile to profile_results.txt...")
    profiler_script = """
import json
import os
import sys
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def run_workload():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    if not os.path.exists(sample_file):
        data = {'data': {'products': [{'id': i, 'name': f'test_{i}', 'price': {'amount': 10}} for i in range(10)]}}
        with open(sample_file, 'w') as f:
            json.dump(data, f)
    else:
        with open(sample_file) as f:
            data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=2)
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 10}

    for _ in range(5):
        processor.process_menu_data(menu_items)

    scraper = CanaData(interactive_mode=False)
    scraper.allMenuItems = {}

    def worker(worker_id):
        local_items = {}
        for i in range(100):
            local_items[f"{worker_id}_{i}"] = [{'id': worker_id * 1000 + i, 'name': 'test'}]
        with scraper._menu_data_lock:
            scraper.allMenuItems.update(local_items)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    run_workload()
"""
    with open('temp_profiler.py', 'w') as f:
        f.write(profiler_script)

    cProfile.run('import temp_profiler; temp_profiler.run_workload()', 'audit_profile.prof')

    with open('profile_results.txt', 'w') as f:
        p = pstats.Stats('audit_profile.prof', stream=f)
        p.strip_dirs().sort_stats('cumulative').print_stats(30)

    print("cProfile results saved to profile_results.txt")
    os.remove('temp_profiler.py')

if __name__ == "__main__":
    profile_codebase()
