import cProfile
import pstats
from CanaData import CanaData

def profile_organize():
    scraper = CanaData()
    scraper.allMenuItems = {
        "loc1": [
            {"id": str(i), "name": f"Item {i}", "prices": {"ounce": [100.0]}} for i in range(1000)
        ]
    }
    scraper.city_slug = "test_slug"

    profiler = cProfile.Profile()
    profiler.enable()
    scraper.organize_into_clean_list()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.strip_dirs().sort_stats('cumulative').print_stats(15)

if __name__ == '__main__':
    profile_organize()
