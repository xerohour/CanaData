
## 2026-03-18 - Pandas Normalization Overhead
**Learning:** Benchmarking identified that `pd.json_normalize` acts as an anti-optimization when flattening deeply nested, small-scope data structures. The overhead of instantiating DataFrames outpaces the pure Python recursive dictionary flattening implementation.
**Action:** Retain native Python Dictionary flattening for menu processing. Do not replace native list/dict comprehensions with Pandas operations unless heavy vectorized math is explicitly required.

## 2026-03-18 - Thread Contention in CanaData
**Learning:** A single coarse `_menu_data_lock` in `CanaData.py` forces all concurrent threads to block sequentially when writing data back to the instance, resulting in severe "noisy neighbor" contention and neutralizing horizontal scaling gains from `ConcurrentMenuProcessor`.
**Action:** Implement fine-grained locks (`_items_lock`, `_empty_lock`, `_strains_lock`, `_count_lock`, `_locations_lock`) to isolate read/writes by domain, allowing overlapping I/O and maximizing horizontal scalability.
