import json

from CanaData import CanaData

sample_file = 'sample_products.json'
with open(sample_file) as f:
    data = json.load(f)

products = data.get('data', {}).get('products', [])

scraper = CanaData(optimize_processing=False, interactive_mode=False)

import time

start = time.perf_counter()
for i in range(100):
    for item in products:
        scraper.flatten_dictionary(item)
end = time.perf_counter()

print(f"Time: {end - start}")
