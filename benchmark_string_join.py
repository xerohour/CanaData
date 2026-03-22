import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'parse-script')))
from CanaParse import CanaParse, FlowerFilter

num_rows = 100000
raw_data = []
for i in range(num_rows):
    row = [f"col{j}" for j in range(30)]
    row[9] = "10.0"
    row[20] = "flower"
    row[29] = "dispensary"
    raw_data.append(row)

p1 = CanaParse(no_filter=True)
p1.raw_data = raw_data
filters = []
for i in range(10):
    f = FlowerFilter()
    f.name = f"Filter {i}"
    f.key = "prices.gram"
    f.price = 20.0
    f.compare = "<="
    f.brands = [f"brand{i}"]
    filters.append(f)
p1.filters = filters

start_time = time.time()
p1.apply_filters()
end_time = time.time()
print(f"Original apply_filters took: {end_time - start_time:.4f} seconds")
