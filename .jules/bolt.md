## 2026-03-15 - Fine-Grained Locks for Concurrency
**Learning:** Using a single monolithic `threading.Lock()` to protect multiple unrelated shared collections creates "noisy neighbor" bottlenecks, degrading parallel scaling.
**Action:** Replaced `_menu_data_lock` with `_items_lock`, `_empty_lock`, `_strains_lock`, `_count_lock`, and `_locations_lock` to protect specific data structures in `CanaData.py`.

## 2026-03-15 - Data Processing Overhead
**Learning:** `pandas.json_normalize` incurs significant overhead when processing deeply nested, small-scoped dictionary structures compared to a pure Python stack-based iteration approach.
**Action:** Recorded benchmark results confirming custom dictionary flattening outperforms Pandas element-wise Series operations for this specific workload.
