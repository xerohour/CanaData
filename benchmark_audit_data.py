import time
from CanaData import CanaData

cd = CanaData(interactive_mode=False, optimize_processing=False)

dummy_items = [{'id': i, 'name': f'item_{i}', 'price': {'amount': 10, 'currency': 'USD'}} for i in range(5000)]
cd.allMenuItems = {'loc1': dummy_items}

start = time.time()
cd._original_organize_into_clean_list()
end = time.time()

print(f"Data Benchmark: {end - start:.4f} seconds")
