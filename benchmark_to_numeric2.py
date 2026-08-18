import time
import pandas as pd
import numpy as np

data = ['50.0'] * 20000 + ['invalid'] * 5000 + [None] * 5000 + ['100'] * 20000
df = pd.DataFrame({'price.amount': data})

start = time.time()
original_col = df['price.amount']
numeric_col = pd.to_numeric(original_col, errors="coerce")
result1 = numeric_col.where(numeric_col.notna(), original_col)
end = time.time()
print(f"Current pd.to_numeric + where Time: {end - start:.6f} seconds")

start = time.time()
result2 = [float(x) if str(x).replace('.', '', 1).isdigit() else x for x in df['price.amount']]
end = time.time()
print(f"List comp isdigit Time: {end - start:.6f} seconds")
