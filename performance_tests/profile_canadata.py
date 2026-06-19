import cProfile
import pstats
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def run_profile():
    cana = CanaData(interactive_mode=False)

    # Load sample data
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    mock_payload = {
        "listing": {"id": "1", "slug": "test-dispensary", "wmid": 123},
        "categories": [{"title": "Test", "items": data.get('data', {}).get('products', [])[:50]}]
    }

    # Run 100 iterations of processing
    for _ in range(100):
        cana.process_menu_json(mock_payload)

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    run_profile()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(20)
