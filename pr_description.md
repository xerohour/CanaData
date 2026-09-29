# ⚡ Bolt: [performance improvement] Optimize Dictionary Flattening Loops

### 💡 What
- Replaced dictionary comprehension and `.update()` with direct assignments in a hot loop within `_flatten_dictionary_custom`.

### 🎯 Why
- **Dictionary updates in hot loop:** In CPython, allocating an intermediate dictionary object just to pass it to `.update()` is slower than directly assigning properties iteratively. When this is hit thousands or millions of times during normalization, the allocation overhead adds significant time.

### 📊 Impact
- Reduced dictionary updating overhead in normalization loops.
- Faster parsing and flattening of deep, nested data sources, improving overall throughput.

### 🔬 Measurement
Run the flattening processes under stress, specifically focusing on complex nested lists (which trigger the modified branches).
