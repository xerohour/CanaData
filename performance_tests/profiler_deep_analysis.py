import cProfile
import io
import json
import os
import pstats
import sys

from memory_profiler import profile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from optimized_data_processor import OptimizedDataProcessor
from CanaData import CanaData


def get_mock_data():
    sample_file = os.path.join(os.path.dirname(__file__), "..", "sample_products.json")
    if os.path.exists(sample_file):
        with open(sample_file) as f:
            return json.load(f)
    return {"data": {"products": [{"id": 1, "name": "test"} for _ in range(100)]}}


def run_processor_profile():
    data = get_mock_data()
    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {"test_dispensary": data.get("data", {}).get("products", []) * 100}

    # Run profiling
    print("Running OptimizedDataProcessor Profiling (Batched Pandas Processing)")
    pr = cProfile.Profile()
    pr.enable()
    processor.process_menu_data(menu_items)
    pr.disable()

    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)
    print(s.getvalue())


@profile
def run_memory_leak_scan():
    print("Scanning for Memory Leaks during processing")
    data = get_mock_data()
    processor = OptimizedDataProcessor(max_workers=4)
    menu_items = {"test_dispensary": data.get("data", {}).get("products", []) * 20}

    for _ in range(15):
        processor.process_menu_data(menu_items)


def run_legacy_profile():
    data = get_mock_data()
    scraper = CanaData(interactive_mode=False, optimize_processing=False)
    products = data.get("data", {}).get("products", []) * 100

    print("Running Legacy Iterative Profiling")
    pr = cProfile.Profile()
    pr.enable()
    for item in products:
        scraper.flatten_dictionary(item)
    pr.disable()

    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)
    print(s.getvalue())


if __name__ == "__main__":
    run_processor_profile()
    run_legacy_profile()
    run_memory_leak_scan()
