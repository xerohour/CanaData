import cProfile
import pstats
import io
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CanaData import CanaData

def run_profiling():
    scraper = CanaData(interactive_mode=False, max_workers=10)
    # mock some locations
    scraper.locationsFound = [{'slug': f'test-{i}', 'id': f'id-{i}'} for i in range(50)]

    def mock_fetch(location):
        return True

    scraper._fetch_and_process_menu = mock_fetch

    pr = cProfile.Profile()
    pr.enable()
    scraper._getMenusConcurrent()
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())

if __name__ == '__main__':
    run_profiling()
