
## 2024-05-24 - Synchronous Requests Bottleneck
**Learning:** Synchronous `requests` block threads and create severe I/O bottlenecks in concurrent loops.
**Action:** Recommend migrating core scraper logic to `aiohttp` and `asyncio` for horizontal scalability.
