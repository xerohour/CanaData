import json

with open("sample_products.json", "r") as f:
    mock_data = json.load(f)

items = (
    mock_data
    if isinstance(mock_data, list)
    else mock_data.get("data", {}).get("products", [])
)
d = items[0]


def orig_flatten():
    result = {}
    stack = [iter(d.items())]  # Stack contains iterators of dictionary items
    keys = []  # Tracks the current path in the dictionary (e.g., ['price', 'amount'])
    while stack:
        for k, v in stack[-1]:
            keys.append(k)
            if isinstance(v, list):
                # Handle lists: if it's a list of dicts, go deeper; if primitives, join them
                if len(v) > 0:
                    for item in v:
                        if item:
                            if isinstance(item, dict):
                                if len(item.keys()) < 1:
                                    result[".".join(keys)] = "None"
                                else:
                                    # Push the nested dict onto the stack
                                    stack.append(iter(item.items()))
                            elif isinstance(item, list):
                                # Fallback for nested lists (semi-unsupported)
                                result[".".join(keys)] = ".".join(item)
                                keys.pop()
                            else:
                                # Primitives in a list are joined by dot notation
                                result[".".join(keys)] = ".".join(str(x) for x in v)
                                keys.pop()
                                break
                    break
                else:
                    result[".".join(keys)] = "None"
                    keys.pop()
            elif isinstance(v, dict):
                # Handle nested dictionaries
                if len(v.keys()) < 1:
                    result[".".join(keys)] = "None"
                    keys.pop()
                else:
                    # Push the nested dict onto the stack
                    stack.append(iter(v.items()))
                    break
            else:
                # Leaf node: Store the value as a string
                result[".".join(keys)] = str(v)
                keys.pop()
        else:
            # Finished processing an iterator: pop the path segment and the iterator itself
            if keys:
                keys.pop()
            stack.pop()
    return result


def rule_optimized_flatten():
    result = {}
    stack = [iter(d.items())]
    keys = []

    # Pre-caching methods per rule
    _dict = dict
    _list = list
    _join = ".".join
    _str = str

    while stack:
        for k, v in stack[-1]:
            keys.append(k)

            if isinstance(v, _list):
                if v:
                    for item in v:
                        if item:
                            if isinstance(item, _dict):
                                if item:
                                    stack.append(iter(item.items()))
                                else:
                                    result[_join(keys)] = "None"
                            elif isinstance(item, _list):
                                result[_join(keys)] = _join(item)
                                keys.pop()
                            else:
                                result[_join(keys)] = _join(_str(x) for x in v)
                                keys.pop()
                                break
                    break
                else:
                    result[_join(keys)] = "None"
                    keys.pop()
            elif isinstance(v, _dict):
                if v:
                    stack.append(iter(v.items()))
                    break
                else:
                    result[_join(keys)] = "None"
                    keys.pop()
            else:
                result[_join(keys)] = _str(v)
                keys.pop()
        else:
            if keys:
                keys.pop()
            stack.pop()
    return result


import timeit

t1 = timeit.timeit(orig_flatten, number=20000)
t2 = timeit.timeit(rule_optimized_flatten, number=20000)
print(f"Original flatten: {t1:.4f}")
print(f"Rule optimized flatten: {t2:.4f}")
print(f"Improvement: {(t1 - t2) / t1 * 100:.2f}%")
