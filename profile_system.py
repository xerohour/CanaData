import cProfile
import pstats
import io
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def profile_target():
    print("Profiling optimized data processor...")
    sample_file = os.path.join(os.path.dirname(__file__), 'sample_products.json')
    if not os.path.exists(sample_file):
        data = {"data": {"products": [{"id": i, "name": f"test_{i}", "price": i} for i in range(100)]}}
    else:
        with open(sample_file) as f:
            data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    # big payload
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 50}

    # run multiple times to get a stable profile
    for _ in range(5):
        processor.process_menu_data(menu_items)

def main():
    pr = cProfile.Profile()
    pr.enable()
    profile_target()
    pr.disable()

    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30) # Top 30

    print(s.getvalue())

    with open("cprofile_output.txt", "w") as f:
        f.write(s.getvalue())

if __name__ == "__main__":
    main()