## Performance Learnings


## 2024-04-16 - Concurrency Bottleneck in CanaData
**Learning:** Centralized thread locking (`_menu_data_lock`) over the `self.allMenuItems` list prevents effective parallel execution during high-volume data accumulation, restricting application to vertical scaling.
**Action:** Future designs should avoid global mutable state or implement asynchronous chunk aggregation prior to merging.

## 2024-05-20 - Global State Locking Bottlenecks
**Learning:** Using a single global lock (`_menu_data_lock`) across threads to manage a stateful dictionary (`allMenuItems`) severely restricts horizontal scaling and creates a "noisy neighbor" problem under high concurrency.
**Action:** In future architectures, avoid stateful single-node locks. Use stateless workers paired with asynchronous message queues (e.g., RabbitMQ, Redis) for distributed data ingestion.
