
## 2025-04-17 - Architectural Scalability and Benchmarking
**Learning:** Legacy `CanaData` uses an in-process global state (`allMenuItems`) protected by a single thread lock (`_menu_data_lock`), creating a "noisy neighbor" vulnerability under high concurrent load that blocks horizontal scaling. The new `OptimizedDataProcessor` uses Pandas DataFrames which is fast for large batches but has high initialization latency (mean ~38.2ms compared to legacy's ~256µs) and is unsuitable for continuous, low-latency single-item ingestion.
**Action:** Transition away from global state arrays to asynchronous message queues (e.g., RabbitMQ, Redis Pub/Sub) with stateless worker nodes for horizontal scaling. Use DataFrame batch processing strictly for large chunks rather than single-item streaming.
