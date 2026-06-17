import sys
import time
import json
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CanaData import CanaData

def generate_mock_data():
    return {
        "id": "12345",
        "name": "Super Lemon Haze",
        "price": {"amount": 50, "currency": "USD"},
        "availability": [{"store_id": "A1", "stock": 10}, {"store_id": "B2", "stock": 0}],
        "metadata": {
            "terpenes": {"myrcene": 0.5, "limonene": 1.2},
            "lab_results": {"thc": 22.5, "cbd": 0.1, "passed": True},
            "empty_dict": {}
        },
        "tags": ["sativa", "citrus", "energy"],
        "empty_list": []
    }

def get_large_payload():
    return {f"k_{i}": {f"inner_{j}": {"deep": [1, 2, 3]} for j in range(10)} for i in range(100)}

def benchmark_flatten():
    c = CanaData()
    data = get_large_payload()

    start = time.time()
    for _ in range(500):
        c.flatten_dictionary(data)
    end = time.time()
    print("Time taken:", end - start)

if __name__ == "__main__":
    benchmark_flatten()
