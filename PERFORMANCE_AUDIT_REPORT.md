# Performance & Scalability Audit Report

## 1. Codebase Profiling

### Inefficient Data Normalization
- **Bottleneck**: The flattening of menu items is highly recursive and CPU-intensive, creating nested dictionaries to arbitrary depths.
- **Root Cause**: In `optimized_data_processor.py`, although Pandas is used, it falls back or pre-processes using expensive conversions (e.g. `isinstance` checks inside loops over thousands of items). The initial custom recursive flattener in `CanaData.py` (`flatten_dictionary`) creates huge overhead for lists and dictionaries.

### Architectural Limits
- **Statefulness**: `CanaData` keeps the entire dataset in memory (`self.allMenuItems`). While processing large states like California, this causes massive heap allocations and potential OOM errors in memory-constrained containers.
- **Concurrency Bottlenecks**: `concurrent_processor.py` relies on `threading.Lock` and `threading.Semaphore`. This works well for a single machine but limits horizontal scaling. Because rate limiting uses an in-memory lock, scaling across multiple servers (e.g., K8s pods) would require a distributed lock (e.g., Redis).

## 2. Performance Benchmarking

### Benchmarking Results
Benchmarks executed via `cProfile`:
- **Flattening 10,000 items**: ~0.48s runtime. The majority of time is spent inside `pandas/io/json/_normalize.py` and `isinstance` checks.
- **Concurrent Network Throughput (Mocked)**: Fetching 100 locations took ~0.30s.

### Optimization Projection
- **Current Architecture**: CPU bound on JSON parsing and flattening, limited to vertical scaling (larger VM instances).
- **Proposed Architecture**: Streaming JSON parsing, avoiding pandas DataFrame overhead when native structures suffice, and using external caching/locking (Redis) for true horizontal scalability.
  - **Projected Latency**: 50% reduction in CPU processing time via tuple-based flattener.
  - **Projected Throughput**: Unlimited scaling with stateless processing.

## 3. Deep Testing & Edge Cases
Current tests cover basic functionalities (`pytest tests/`). Edge case recommendations:
- High-concurrency race condition testing.
- Rate limit exhaustion simulation in distributed environments.

## 4. Scalability Analytics
- **"Noisy Neighbor" Risk**: Heavy DataFrame processing on shared container instances can choke I/O threads, slowing down parallel network fetches.
- **Elasticity**: Blocked by stateful accumulators (`self.allMenuItems` / `self.results`).

*This report provides the foundation for future micro-optimizations and architectural shifts.*
