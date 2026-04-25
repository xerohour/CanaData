import cProfile
from CanaData import CanaData
import json
import os

if __name__ == "__main__":
    sample_file = os.path.join(os.path.dirname(__file__), '..', 'sample_products.json')
    with open(sample_file) as f:
        data = json.load(f)

    scraper = CanaData(optimize_processing=False, interactive_mode=False)
    products = data.get('data', {}).get('products', [])

    def profile_flatten():
        for item in products:
            scraper.flatten_dictionary(item)

    cProfile.run('profile_flatten()', sort='cumtime')
