import pandas as pd
import json

df = pd.DataFrame({'a': [{'k': 1}, {'k': 2}], 'b': [1, 2]}, index=[0, 0])
first_idx = df['a'].first_valid_index()
val = df['a'].loc[first_idx]
print(type(val))
if isinstance(val, pd.Series):
    val = val.iloc[0]
print(type(val))
