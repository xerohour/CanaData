## 2024-05-05 - Fix Thread Lock Contention
**Learning:** Global mutable arrays protected by thread locks create synchronous bottlenecks ("noisy neighbor" problem) during horizontal scaling and high concurrency, preventing true parallel throughput.
**Action:** Shift to stateless worker nodes where worker threads return results individually, and the main thread aggregates them without locks, ensuring safe and unblocked execution.
