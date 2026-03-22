import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'parse-script')))
from CanaParse import CanaParse, FlowerFilter

num_rows = 100000
raw_data = []
for i in range(num_rows):
    row = [f"col{j}" for j in range(30)]
    row[9] = "10.0"
    row[20] = "flower"
    row[29] = "dispensary"
    raw_data.append(row)

p1 = CanaParse(no_filter=True)
p1.raw_data = raw_data
filters = []
for i in range(10):
    f = FlowerFilter()
    f.name = f"Filter {i}"
    f.key = "prices.gram"
    f.price = 20.0
    f.compare = "<="
    f.brands = [f"brand{i}"]
    filters.append(f)
p1.filters = filters

def apply_filters_optimized(self):
    if not self.raw_data:
        if not self.load_csv_data():
            return

    # PRECALCULATE ROW STRINGS ONCE
    # Instead of joining inside is_match for every filter
    row_strings = [" ".join([str(x) for x in row]).lower() for row in self.raw_data]

    self.filtered_tables = []
    for f in self.filters:
        price_col = self.get_col_by_key(f.key)

        filtered = []
        for i, row in enumerate(self.raw_data):
            if self.is_match_optimized(row, f, price_col, row_strings[i]):
                filtered.append(row[:])

        if f.limit_results_amt > -1 and len(filtered) > f.limit_results_amt:
            filtered = sorted(filtered, key=lambda x: float(str(x[price_col])) if str(x[price_col]).replace('.','',1).isdigit() else 999999)
            filtered = filtered[:f.limit_results_amt]

        self.filtered_tables.append(filtered)

def is_match_optimized(self, row, f, price_col, row_str):
    # 1. Price Comparison
    if f.price:
        row_price_raw = str(row[price_col])
        row_price = float(row_price_raw) if row_price_raw.replace('.','',1).isdigit() else 0
        from CanaParse import getComparisonVal
        if not getComparisonVal(f.compare, row_price, f.price):
            return False

    # 2. Categories (Index 20)
    if f.categories:
        if str(row[20]).lower() not in [c.lower() for c in f.categories]:
            return False

    # 4. Brands
    if f.brands:
        if not any(brand.lower() in row_str for brand in f.brands):
            return False

    # 5. Strains
    if f.strains:
        if not any(strain.lower() in row_str for strain in f.strains):
            return False

    # 6. Stores (Index 29)
    if f.stores:
        if not any(store.lower() in str(row[29]).lower() for store in f.stores):
            return False

    # 7. Bad Words (Exclusion)
    if f.bad_words:
        if any(word.lower() in row_str for word in f.bad_words):
            return False

    # 8. Good Words (Required)
    if f.good_words:
        if not any(word.lower() in row_str for word in f.good_words):
            return False

    # 9. THC Floor
    if f.thc_floor > 0:
        thc_val = self.extract_cannabinoid(row_str, 'thc')
        if thc_val < f.thc_floor:
            if f.thc_floor_strict: return False
        else:
            row.append(f"thc+{thc_val}")

    # 10. CBD Floor
    if f.cbd_floor > 0.001:
        cbd_val = self.extract_cannabinoid(row_str, 'cbd')
        if cbd_val < f.cbd_floor:
            if f.cbd_floor_strict: return False
        else:
            row.append(f"cbd+{cbd_val}")

    return True

p1.apply_filters = apply_filters_optimized.__get__(p1, CanaParse)
p1.is_match_optimized = is_match_optimized.__get__(p1, CanaParse)

start_time = time.time()
p1.apply_filters()
end_time = time.time()
print(f"Optimized apply_filters took: {end_time - start_time:.4f} seconds")
