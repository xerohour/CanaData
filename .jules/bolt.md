
## 2024-03-02 - Pandas to_dict('records') is extremely slow for large DataFrames
**Learning:** `df.to_dict('records')` performs very poorly on DataFrames with many rows (e.g., 100k+). A list comprehension with `zip` and `itertuples()` is significantly faster (often 50%+ reduction in time).
**Action:** When converting large pandas DataFrames to a list of dictionaries, use `[dict(zip(df.columns, row)) for row in df.itertuples(index=False, name=None)]` instead of `df.to_dict('records')`.

## 2024-03-02 - pd.json_normalize list un-flattening is slow when done manually later
**Learning:** `pd.json_normalize` handles nested dictionaries exceptionally well, but does not flatten lists. If those lists are iterated over and converted to strings post-normalization via `df.apply` (e.g., a custom `_handle_remaining_nesting` method), it becomes a major bottleneck due to pandas' slow column-wise apply functions.
**Action:** Pre-process the dictionaries by converting list values to JSON strings using `json.dumps()` *before* passing the list of dictionaries to `pd.json_normalize`.
