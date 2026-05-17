import cProfile
import pstats
import io
import json
import os
import sys

# Ensure root directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

def profile_legacy(products):
    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    for item in products:
        scraper.flatten_dictionary(item)

def profile_optimized(products):
    processor = OptimizedDataProcessor(max_workers=4)
    processor.process_menu_data({'test_location': products})

if __name__ == '__main__':
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    # Replicate the data to make the profile run longer
    products = data.get('data', {}).get('products', []) * 10

    print("Profiling Legacy Method...")
    pr_legacy = cProfile.Profile()
    pr_legacy.enable()
    profile_legacy(products)
    pr_legacy.disable()

    s_legacy = io.StringIO()
    ps_legacy = pstats.Stats(pr_legacy, stream=s_legacy).sort_stats('tottime')
    ps_legacy.print_stats(10)
    print(s_legacy.getvalue())

    print("Profiling Optimized Method...")
    pr_opt = cProfile.Profile()
    pr_opt.enable()
    profile_optimized(products)
    pr_opt.disable()

    s_opt = io.StringIO()
    ps_opt = pstats.Stats(pr_opt, stream=s_opt).sort_stats('tottime')
    ps_opt.print_stats(10)
    print(s_opt.getvalue())
