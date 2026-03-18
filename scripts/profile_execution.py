import cProfile
import pstats
from memory_profiler import profile
import pandas as pd
from CanaData import CanaData
from optimized_data_processor import OptimizedDataProcessor

# Prepare data
def prepare_data():
    # We will generate a larger mock payload to get meaningful profiling
    # Load the mock_data.csv as a starting point, but convert it into the format expected by CanaData
    df = pd.read_csv('mock_data.csv')

    mock_items = []
    for i in range(100): # Multiply the data
        for _, row in df.iterrows():
            item = {
                'name': f"{row.get('name', 'Unknown')} {i}",
                'description': row.get('description', ''),
                'price': {'amount': float(row.get('price_eighth', 0) or 0), 'currency': 'USD'},
                'strain_data': {'name': 'test strain', 'slug': f'test-strain-{i}'},
                'tags': ['a', 'b', 'c', 'd'],
                'category': row.get('category', ''),
                'images': [{'url': str(row.get('image_url', ''))}],
            }
            mock_items.append(item)

    all_menu_items = {
        f'location_{j}': mock_items.copy() for j in range(10)
    }
    return all_menu_items

@profile
def run_memory_profiling(all_menu_items):
    print("Running memory profiling...")
    processor = OptimizedDataProcessor(max_workers=4)
    # Test optimized processing
    processor.process_menu_data(all_menu_items)

    # Test original processing
    cana = CanaData()
    cana.allMenuItems = all_menu_items
    cana._original_organize_into_clean_list()

def run_cpu_profiling(all_menu_items):
    print("Running CPU profiling...")
    profiler = cProfile.Profile()
    profiler.enable()

    processor = OptimizedDataProcessor(max_workers=4)
    processor.process_menu_data(all_menu_items)

    cana = CanaData()
    cana.allMenuItems = all_menu_items
    cana._original_organize_into_clean_list()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(30)

if __name__ == "__main__":
    all_menu_items = prepare_data()
    run_cpu_profiling(all_menu_items)
    run_memory_profiling(all_menu_items)
