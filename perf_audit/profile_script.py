import cProfile
import pstats
import io
import time
import sys
import os
sys.path.append(os.path.abspath('.'))
from CanaData import CanaData

def main():
    start = time.time()
    cana = CanaData()
    cana.slug = "los-angeles"
    cana.allMenuItems = {"los-angeles-dispensary": [{"test": {"nested": "value"}}, {"test2": "value2"}]}
    cana._original_organize_into_clean_list()
    end = time.time()
    print(f"Elapsed: {end - start:.2f}s")

if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    with open('perf_audit/profile_results.txt', 'w') as f:
        f.write(s.getvalue())
