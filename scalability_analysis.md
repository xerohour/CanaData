# Scalability Analysis

## Stateful Components
The `CanaData` class stores processed menu items in memory (`self.allMenuItems`, `self.totalLocations`), which is protected by a threading lock (`self._menu_data_lock`).

## Horizontal Scaling Potential
This statefulness prevents true horizontal scaling across distributed instances without a centralized datastore (like Redis or PostgreSQL). The current design limits processing to what can fit in the RAM of a single VM.

## Noisy Neighbors
The `threading.Lock()` causes thread contention under high workloads. Rate-limiting is handled globally within the application, which could bottleneck if multiple instances share the same IP/API keys.
