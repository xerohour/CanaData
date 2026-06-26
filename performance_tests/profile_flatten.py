import cProfile
import pstats
import json
import os
import sys

# Ensure root directory is in path for imports to work during CI
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def main():
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])

    profiler = cProfile.Profile()
    profiler.enable()

    for item in products:
        scraper.flatten_dictionary(item)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(20)

if __name__ == '__main__':
    main()
