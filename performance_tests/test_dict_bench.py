import cProfile
import pstats
import time
from CanaData import CanaData

def generate_data():
    return {
        "nested_dict": {"a": {"b": {"c": 1}}},
        "nested_list": [{"id": 1}, {"id": 2}],
        "simple_list": [1, 2, 3],
        "empty_dict": {},
        "empty_list": [],
        "primitive": "value"
    }

def run_profile():
    data = generate_data()
    cana = CanaData()
    start_time = time.time()
    for _ in range(100000):
        cana.flatten_dictionary(data)
    end_time = time.time()
    print(f"Dict flattening execution time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    cProfile.run("run_profile()", "dict.prof")
    p = pstats.Stats("dict.prof")
    p.strip_dirs().sort_stats("cumulative").print_stats(20)
