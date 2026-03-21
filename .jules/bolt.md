## 2026-02-24 - Network Connection Pooling
**Learning:** Instantiating new `requests.get()` connections for high-frequency API calls causes network I/O bottlenecks and connection exhaustion.
**Action:** Configure and reuse a `requests.Session()` with an `HTTPAdapter` matching the `max_workers` limits to keep HTTP connections alive and pool them efficiently.

## 2026-02-24 - Pandas String Optimization
**Learning:** Using Pandas `apply` with arbitrary Python functions (like `json.dumps`) has significant object overhead that negates Pandas' performance benefits.
**Action:** Replace Pandas `apply` calls involving `json.dumps` with pure Python list comprehensions to bypass the Series object overhead.

## 2026-02-24 - String Joining in Loops
**Learning:** Redundant string joining inside an inner loop (e.g., in `CanaParse.apply_filters`) is computationally expensive and degrades performance over large datasets.
**Action:** Pre-calculate operations like `row_str` outside of the innermost filter evaluation block to eliminate redundant evaluations.

## 2026-02-24 - Shallow Copy Evaluation Delay
**Learning:** Proactively creating shallow copies (`row[:]`) of every item in a dataset before evaluating a filter condition results in heavy memory churn and latency.
**Action:** Evaluate the condition against the original row first, and only append a copy `original_row[:]` upon a successful match to conserve memory and time.
