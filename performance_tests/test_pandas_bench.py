import cProfile
import pstats
import time
import json
from optimized_data_processor import OptimizedDataProcessor

def generate_data():
    all_menu_items = {}
    for i in range(100):
        all_menu_items[f"loc_{i}"] = [
            {
                "id": j,
                "name": f"Product {j}",
                "price": 10.99,
                "nested_dict": {"key": "value", "sub": {"a": 1}},
                "nested_list": [{"id": 1}, {"id": 2}],
                "none_val": None,
                "simple_list": [1, 2, 3]
            } for j in range(200)
        ]
    return all_menu_items

def run_profile():
    data = generate_data()
    processor = OptimizedDataProcessor(max_workers=4)
    start_time = time.time()
    processor.process_menu_data(data)
    end_time = time.time()
    print(f"Pandas processing execution time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    cProfile.run("run_profile()", "pandas.prof")
    p = pstats.Stats("pandas.prof")
    p.strip_dirs().sort_stats("cumulative").print_stats(20)
