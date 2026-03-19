## 2026-03-19 - Network Connection Pooling ("Noisy Neighbor" I/O)
**Learning:** Instantiating `requests.get()` across 10-20 concurrent worker threads causes severe port exhaustion and TLS handshake latencies, effectively bottlenecking parallel API fetchers.
**Action:** Always instantiate a persistent `requests.Session()` mounted with an `HTTPAdapter` configured with `pool_connections` and `pool_maxsize` directly mapped to the thread pool size (`self.max_workers`).

## 2026-03-19 - Concurrency Data Mapping Bottlenecks
**Learning:** Using a single monolithic lock (`_menu_data_lock`) over multiple disparate data structures forces all concurrent workers to process mapping logic serially, destroying horizontal scaling benefits and creating high lock acquisition wait times.
**Action:** Replace single shared locks with fine-grained locks (e.g., `_items_lock`, `_empty_lock`, `_strains_lock`) and reduce lock block scope strictly to the mutation operation rather than wrapping the entire data processing logic.

## 2026-03-19 - Data Processing Overhead (Pandas vs Pure Python)
**Learning:** `pandas.Series.apply` incurs massive overhead when mapping generic Python functions (like `json.dumps`) element-wise over columns containing lists/dicts, compared to native Python list comprehensions.
**Action:** When handling remaining nested structures that `json_normalize` missed, bypass `pandas.Series.apply` by extracting to a native Python list and performing a list comprehension: `df[col] = [json.dumps(x) if isinstance(...) else str(x) for x in df[col].tolist()]`.