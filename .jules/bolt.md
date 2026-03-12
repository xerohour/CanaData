
## 2026-03-12 - Performance Audit Learnings
**Learning:** Application is highly I/O bound. The biggest bottlenecks are network requests and `curl` fallback subprocesses, not the `pandas` or pure-Python data processing. CPU bottlenecks do not appear to exist in the current flattening logic for normal workloads.
**Action:** Prioritize caching, concurrent worker limits, and network tuning (retries, timeouts) when evaluating scalability, rather than micro-optimizing algorithms for dataframe formatting.
