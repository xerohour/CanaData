import sys
import time
from CanaData import CanaData

print("Testing initialization overhead...")
start = time.time()
scraper = CanaData(interactive_mode=False)
print(f"Init took {time.time() - start:.4f}s")
