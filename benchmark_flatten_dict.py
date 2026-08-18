import time
import json
from optimized_data_processor import OptimizedDataProcessor

def generate_data():
    all_menu_items = {}
    for loc_id in range(100):
        items = []
        for item_id in range(500):
            item = {
                "id": f"item_{item_id}",
                "name": f"Product {item_id}",
                "price": {"amount": 50.0, "currency": "USD"},
                "metadata": {"brand": "BrandX", "tags": ["tag1", "tag2"]},
                "nested_list": [{"k": "v"}],
                "deeply_nested": {"a": {"b": {"c": 1}}}
            }
            items.append(item)
        all_menu_items[f"loc_{loc_id}"] = items
    return all_menu_items

data = generate_data()

items_with_location = [
    {**item, "_location_id": location_id}
    for location_id, items in data.items()
    for item in items
]

processor = OptimizedDataProcessor()
start = time.time()
for item in items_with_location:
    processor._flatten_dictionary_custom(item)
end = time.time()
print(f"Original Custom Flatten Time: {end - start:.4f} seconds")

def fast_flatten(d):
    result = {}
    stack = [iter(d.items())]
    keys = []

    while stack:
        for k, v in stack[-1]:
            key = ".".join(keys + [k]) if keys else k

            if isinstance(v, dict):
                keys.append(k)
                stack.append(iter(v.items()))
                break
            elif isinstance(v, list):
                if v and isinstance(v[0], dict):
                    if len(v) == 1:
                        # Changed .update to explicit loop
                        for sub_k, sub_v in v[0].items():
                            result[f"{k}.{sub_k}"] = sub_v
                    else:
                        result[key] = json.dumps(v)
                else:
                    result[key] = str(v) if v else "None"
            elif v is None:
                result[key] = "None"
            else:
                result[key] = str(v)
        else:
            if len(stack) > 1:
                keys.pop()
            stack.pop()

    return result

start = time.time()
for item in items_with_location:
    fast_flatten(item)
end = time.time()
print(f"Optimized Custom Flatten Time: {end - start:.4f} seconds")
