
## 2024-05-03 - Identified Thread Contention in CanaData Global State
**Learning:** Found that CanaData uses a global array (`allMenuItems`) synced with a single lock (`_menu_data_lock`) for data aggregation across threads. This creates massive thread contention (lock queuing) and halts horizontal scalability. Using raw locks to guard global lists in threaded I/O bounds python operations creates a severe noisy neighbor bottleneck under high volume.
**Action:** Always advocate for lock-free asynchronous queues (e.g., Python's `queue.Queue`, or external brokers like RabbitMQ) instead of mutex-guarded global lists when designing horizontally scalable concurrent data ingest pipelines.
