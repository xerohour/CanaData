import cProfile
import pstats

from cache_manager import CacheManager
from optimized_data_processor import OptimizedDataProcessor


def run_cache_profiling():
    cache = CacheManager(memory_cache_size=10000, enable_disk_cache=False)
    for i in range(10000):
        cache.set(f"key_{i}", {"val": i})
        cache.get(f"key_{i}")

def run_processor_profiling():
    processor = OptimizedDataProcessor(max_workers=2)
    items = []
    for i in range(1000):
        items.append({
            "id": i,
            "price": {"amount": 25.0},
            "tags": [{"name": "A"}, {"name": "B"}]
        })
    processor.process_menu_data({"loc_1": items})

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run_cache_profiling()
    run_processor_profiling()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.dump_stats('audit_profile.prof')
    with open('audit_profile.txt', 'w') as f:
        stats = pstats.Stats('audit_profile.prof', stream=f)
        stats.sort_stats('cumtime').print_stats(30)
