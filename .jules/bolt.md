## 2024-05-18 - Improve CanaData Concurrency

**Learning:** Using a single shared lock (`_menu_data_lock`) creates "noisy neighbor" concurrency bottlenecks and limits horizontal scaling when multiple threads are trying to process and map data simultaneously.

**Action:** Refactored lock logic in CanaData.py to use fine-grained locks (`_items_lock`, `_empty_lock`, `_strains_lock`, `_count_lock`, `_locations_lock`) to allow for better concurrent processing and improved thread safety without blocking unnecessary operations.