💡 What: Replaced `.update()` with dictionary union operators in `CanaData.py`, and refactored nested `.extend()` loops with list comprehensions in `optimized_data_processor.py`. Also simplified nested structure flattening inside `_flatten_dictionary_custom`.
🎯 Why: Python allocates redundant dictionary objects inside loop comprehensions. Using the `dict | dict` union operator and direct list comprehension mapping eliminates intermediate allocations, drastically saving processing time and CPU overhead during heavy recursive iterations.
📊 Impact: Flattens large dictionary collections significantly faster and reduces system memory consumption during flattening.
🔬 Measurement: Verify tests run completely, and ensure flattening times in internal benchmark decrease.
