1. **Analyze optimization opportunities:**
    - I've discovered that the codebase's `OptimizedDataProcessor.process_menu_data` relies heavily on Pandas (via `pd.json_normalize` and internal iterations) which adds massive overhead due to Pandas Dataframe creation, internal type checking, and slow memory allocations for what essentially constitutes simple dictionary flattening.
    - My benchmarks demonstrate that converting the normalization into pure native Python using a combination of the existing `_flatten_dictionary_custom` with list comprehensions and dictionary unpacking (`{**template_dict, **item}`) is more than **2x faster** than the Pandas implementation.
    - The task is to act as **Bolt** and implement ONE performance improvement. Optimizing `OptimizedDataProcessor.process_menu_data` to use pure Python fits the criteria perfectly.

2. **Rewrite `process_menu_data` in `optimized_data_processor.py`**:
    - Update `OptimizedDataProcessor.process_menu_data` to bypass pandas overhead by implementing the fast pure Python approach, directly leveraging `self._flatten_dictionary_custom`.
    - I will replace the Pandas `json_normalize` and dataframe operations with a simple, high-performance pure-Python implementation using list comprehensions and dict unpacking.

3. **Verify the optimization**:
    - Run the project's tests (`/home/jules/.pyenv/versions/3.12.13/bin/python -m pytest tests/ -v`) to confirm the data output matches the expected behavior and no regressions occur.
    - Run the linter/formatter (`flake8 .` or project equivalent) to ensure standard compliance.

4. **Update `.jules/bolt.md`**:
    - Add a journal entry for the critical learning: "Flattening and normalizing large, predictable JSON API payloads into dictionaries or CSV-ready structures is drastically faster using pure Python list comprehensions and dictionary unpacking (`{**template, **item}`) over Pandas' `json_normalize()`."

5. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done**:
    - Ensure all tests pass.
    - Validate `.jules/bolt.md` is updated.
    - Verify files are free of temporary artifacts.

6. **Submit PR**:
    - Use title "⚡ Bolt: [performance improvement]"
    - Embed PR description strictly following the persona's required formatting.
