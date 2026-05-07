## 2024-05-07 - Remove global thread lock for batched ingestion
**Learning:** The central lock `_menu_data_lock` was causing thread contention ("noisy neighbor") under horizontal scaling and high concurrency, throttling performance. Modifying the worker functions to be stateless and aggregating in the main thread avoids this bottleneck.
**Action:** Always prefer stateless workers returning data to be aggregated by the main thread over using a global state and locks in concurrent architectures.
