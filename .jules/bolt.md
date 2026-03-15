## 2024-03-15 - [Optimize network I/O with connection pooling]
**Learning:** High-frequency API calls via `requests.get()` create significant network I/O overhead due to constant TCP connection setup and teardown.
**Action:** Use `requests.Session()` to enable HTTP Keep-Alive and connection pooling across all network requests.
