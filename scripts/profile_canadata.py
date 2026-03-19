import cProfile
import pstats
from io import StringIO
import time
from unittest.mock import patch
import os
import sys

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def main():
    os.environ['RATE_LIMIT'] = '0'
    os.environ['MAX_WORKERS'] = '20'
    os.environ['USE_CONCURRENT_PROCESSING'] = 'true'

    num_locations = 1000 # Increased to simulate more load
    mock_locations = [{'id': str(i), 'wmid': f'wmid-{i}', 'slug': f'loc-{i}', 'type': 'dispensary', 'name': f'Loc {i}', 'state': 'CA', 'city': 'LA'} for i in range(num_locations)]

    num_items_per_loc = 50 # Increased to simulate more data processing

    def simulate_do_request(url, use_cache=True):
        time.sleep(0.01) # Simulate network latency 10ms
        if 'menu_items' in url:
            items = [{'id': f'item-{i}', 'name': f'Item {i}', 'price': {'amount': 10}, 'brand': {'name': 'BrandX', 'id': '456'}, 'variants': [{'price': 10, 'weight': '1g'}, {'price': 20, 'weight': '3.5g'}], 'deep': {'nested': {'property': 'value'}}} for i in range(num_items_per_loc)]
            return {'data': {'menu_items': items}, 'meta': {'total_menu_items': num_items_per_loc}}
        return None

    pr = cProfile.Profile()
    pr.enable()

    cana = CanaData(interactive_mode=False)
    cana.locations = mock_locations
    cana.NonGreenState = False

    with patch.object(cana, 'do_request', side_effect=simulate_do_request):
        cana.getMenus()

    pr.disable()

    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30)
    print(s.getvalue())

if __name__ == '__main__':
    main()
