## 2024-03-17 - Use Connection Pooling for API Requests
**Learning:** To mitigate network I/O bottlenecks when making high-frequency API calls (e.g., in `CanaData` or `CannMenusClient`), always use `requests.Session()` to enable HTTP Keep-Alive and connection pooling rather than instantiating new `requests.get()` connections.
**Action:** Replace `requests.get()` calls with `session.get()` where `session = requests.Session()` is initialized once per client instance.
