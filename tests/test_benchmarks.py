import pytest
import time
from CanaData import CanaData

def test_large_dictionary_flattening(benchmark):
    cana = CanaData()
    nested_data = {
        "id": 12345, "name": "Super Lemon Haze",
        "brand": {"name": "Brand A", "details": {"established": 2010}},
        "prices": {"gram": 15.0, "eighth": 45.0},
        "strains": [{"id": 1, "name": "Lemon Skunk"}],
        "effects": ["energetic", "happy"]
    }
    benchmark(cana.flatten_dictionary, nested_data)
