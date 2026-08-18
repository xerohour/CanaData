import time
import pandas as pd
import numpy as np

# Generate a large column with a mix of string and numeric values
data = ['50.0'] * 20000 + ['invalid'] * 5000 + [None] * 5000 + ['100'] * 20000
df = pd.DataFrame({'price.amount': data})

# Current implementation
start = time.time()
original_col = df['price.amount']
numeric_col = pd.to_numeric(original_col, errors="coerce")
result1 = numeric_col.where(numeric_col.notna(), original_col)
end = time.time()
print(f"Current pd.to_numeric + where Time: {end - start:.6f} seconds")

# to_numpy approach but checking for None explicitly and without float casting on None
start = time.time()
_isinstance = isinstance
def fast_convert(val):
    if val is None or val == "None":
        return val
    try:
        f = float(val)
        i = int(f)
        return i if i == f else f
    except (ValueError, TypeError):
        return val

result2 = [fast_convert(x) for x in df['price.amount'].to_numpy()]
end = time.time()
print(f"List comp to_numpy Time: {end - start:.6f} seconds")

# to_numpy caching
start = time.time()
_float = float
_int = int

def fast_convert_cached(val):
    if val is None or val == "None":
        return val
    try:
        f = _float(val)
        i = _int(f)
        return i if i == f else f
    except (ValueError, TypeError):
        return val

result3 = [fast_convert_cached(x) for x in df['price.amount'].to_numpy()]
end = time.time()
print(f"List comp to_numpy cached Time: {end - start:.6f} seconds")
