## 2024-03-05 - Connection Pooling Overhead

**Learning:** When making hundreds of API calls to a single domain (like Weedmaps or CannMenus), creating a new `requests.get` instance each time establishes a new TCP and TLS connection, which adds substantial overhead (often 50%+ of the total request time). The codebase's original implementation suffered from this bottleneck.
**Action:** Always use `requests.Session()` to enable HTTP Keep-Alive, allowing subsequent requests to reuse the established underlying connection. Implement this globally across data processing clients.