import cProfile
import pstats
from CanaData import CanaData

def main():
    scraper = CanaData(interactive_mode=False)
    scraper.searchSlug = "boston"
    scraper.storefronts = True
    scraper.deliveries = False
    scraper.getLocations()
    scraper.getMenus()

if __name__ == "__main__":
    cProfile.run("main()", "profile_stats.prof")
    p = pstats.Stats("profile_stats.prof")
    p.strip_dirs().sort_stats("time").print_stats(20)
