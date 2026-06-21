import cProfile
import pstats
import json
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

from optimized_data_processor import OptimizedDataProcessor

def test_profile_optimization():
    sample_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    processor = OptimizedDataProcessor(max_workers=4)
    # Scale up data to get meaningful profiling
    menu_items = {'test_dispensary': data.get('data', {}).get('products', []) * 50}

    profiler = cProfile.Profile()
    profiler.enable()
    processor.process_menu_data(menu_items)
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats('cumtime')
    assert stats.total_calls > 0
