import cProfile
import pstats
import io
import time
from CanaData import CanaData

def run_profiler():
    print("Starting cProfile on CanaData processing...")

    cana = CanaData(max_workers=5, rate_limit=0, cache_enabled=False)
    cana.searchSlug = "test-slug"

    # Mock network layer to isolate CPU profiling
    def mock_do_request(url, use_cache=False):
        time.sleep(0.01) # Simulate network IO
        if "offset" in url:
            # First request returns listings
            if cana.locationsFound == 0:
                return {
                    'meta': {'total_listings': 5},
                    'data': {'listings': [
                        {'id': f'loc-{i}', 'wmid': f'wmid-{i}', 'slug': f'loc-{i}', 'type': 'dispensary'}
                        for i in range(5)
                    ]}
                }
            return 'break'
        elif "menu_items" in url:
            return {
                'meta': {'total_menu_items': 100},
                'data': {'menu_items': [
                    {
                        'id': f'item-{i}',
                        'name': f'Product {i}',
                        'price': {'amount': 10},
                        'strain_data': {'slug': f'strain-{i}'}
                    } for i in range(100)
                ]}
            }
        return False

    cana.do_request = mock_do_request

    # Profile the main workflow
    pr = cProfile.Profile()
    pr.enable()

    cana.get_locations()
    cana.get_menus()
    cana.data_to_csv()

    pr.disable()

    s = io.StringIO()
    sortby = 'cumtime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(30) # Print top 30

    with open('output/profile_results.txt', 'w') as f:
        f.write(s.getvalue())

    print("Profiling complete. Results written to output/profile_results.txt")

if __name__ == "__main__":
    run_profiler()
