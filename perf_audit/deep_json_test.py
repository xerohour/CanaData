import time
import sys
import os
sys.path.append(os.path.abspath('.'))
from CanaData import CanaData

def create_deep_dict(depth):
    d = {"value": "end"}
    for i in range(depth):
        d = {f"level_{depth-i}": d}
    return d

def main():
    cana = CanaData()
    for depth in [10, 50, 100, 500]:
        deep_dict = create_deep_dict(depth)
        start = time.time()
        try:
            flat = cana.flatten_dictionary(deep_dict)
            end = time.time()
            print(f"Depth: {depth:3d} | Time: {end - start:.4f}s | Keys generated: {len(flat)}")
        except RecursionError:
            print(f"Depth: {depth:3d} | FAILED: RecursionError")

if __name__ == "__main__":
    main()
