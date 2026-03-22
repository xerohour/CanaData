## 2026-02-17 - Optimize Network Connection Pooling
**Learning:** Initializing `requests.get()` inside high-frequency asynchronous loops or concurrent executors fails to reuse TCP connections, causing significant latency overhead due to constant handshaking and potential port exhaustion.
**Action:** When making concurrent API calls (e.g., `CanaData` or `CachedAPIClient`), always instantiate a `requests.Session()` and mount an `HTTPAdapter` configured with `pool_maxsize` and `pool_connections` matching the concurrency `max_workers` limit. Update methods like `do_request` to call `self.session.get`.

## 2026-02-17 - Optimize Memory and Pandas List Overhead
**Learning:**
1. Redundant string joining inside an inner loop over rows x filters drastically slows down large dataset evaluations.
2. Shallow copying rows `row[:]` upfront before matching conditions artificially balloons memory requirements.
3. Pandas Series methods like `df[col].apply()` introduce severe Series overhead for row-by-row string operations.
**Action:**
1. Precalculate `row_str` for all rows before entering filter loops.
2. Evaluate conditions on the original row reference and only create a shallow copy upon a successful match `filtered.append(original_row[:])`.
3. Bypass Pandas Series `.apply()` overhead for element-wise string manipulations by substituting with pure Python list comprehensions `df[col] = [manipulate(x) for x in df[col]]`.