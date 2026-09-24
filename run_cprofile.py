import cProfile
import pstats
from io import StringIO

from optimized_data_processor import OptimizedDataProcessor


def run_profiling():
    processor = OptimizedDataProcessor()

    mock_item_data = {
        "id": "item123",
        "name": "Super Silver Haze",
        "price": {"price_grams": [{"grams": 1, "price": 15.0}]},
        "thc": "25%",
        "brand": {"name": "BestBrand"},
        "category": {"name": "Flower"},
    }

    batch = {"loc1": [mock_item_data.copy() for _ in range(5000)]}

    profiler = cProfile.Profile()
    profiler.enable()

    processor.process_menu_data(batch)

    profiler.disable()

    s = StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    ps.print_stats(30)
    print(s.getvalue())


if __name__ == "__main__":
    run_profiling()
