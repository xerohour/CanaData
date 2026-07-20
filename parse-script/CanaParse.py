import os
import csv
import re
import json
import logging
import argparse
import glob
from datetime import datetime
from typing import List, Any
from yattag import Doc, indent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FlowerFilter:
    """
    Configuration for filtering cannabis products.
    """

    def __init__(self, filter_data=None):
        self.table_sort_col = ""
        self.limit_results_amt = -1
        self.limit_results_amt_email = -1
        self.name = ""
        self.key = ""
        self.compare = ""
        self.price = 0.0
        self.categories = []
        self.brands = []
        self.stores = []
        self.strains = []
        self.bad_words = []
        self.good_words = []
        self.priority_words = []
        self.thc_floor = 0
        self.cbd_floor = 0.0
        self.thc_floor_strict = False
        self.cbd_floor_strict = False
        self.terpenes = []

        if filter_data:
            self.load_from_dict(filter_data)

    def load_from_dict(self, data):
        """Populate filter attributes from a dictionary."""
        self.table_sort_col = str(data.get("table_sort_col", ""))
        self.limit_results_amt = int(data.get("limit_results_amt", -1))
        self.limit_results_amt_email = int(
            data.get("limit_results_amt_email", -1))
        self.name = str(data.get("name", ""))
        self.key = str(data.get("key", ""))
        self.compare = str(data.get("compare", ""))
        self.price = float(data.get("price", 0.0))
        self.categories = data.get("categories", [])
        self.brands = data.get("brands", [])
        self.stores = data.get("stores", [])
        self.strains = data.get("strains", [])
        self.bad_words = data.get("bad_words", [])
        self.good_words = data.get("good_words", [])
        self.priority_words = data.get("priority_words", [])
        self.thc_floor = int(data.get("thc_floor", 0))
        self.cbd_floor = float(data.get("cbd_floor", 0.0))
        self.thc_floor_strict = bool(data.get("thc_floor_strict", False))
        self.cbd_floor_strict = bool(data.get("cbd_floor_strict", False))
        self.terpenes = data.get("terpenes", [])


class CanaParse:
    """
    Main class for parsing CanaData CSV results and generating HTML reports.
    """

    def __init__(self, csv_file=None, csv_folder=None, no_filter=False):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_file = csv_file or os.getenv(
            'CSV_FILE', 'colorado_results.csv')
        self.csv_folder = csv_folder or os.getenv('CSV_FOLDER', os.path.join(
            base_dir, f"CanaData_{datetime.today().strftime('%m-%d-%Y')}"))
        self.no_filter = no_filter
        self.filters = []
        self.raw_data: List[List[Any]] = []
        self.filtered_tables: List[List[List[Any]]] = []
        self.header_map = {}
        self.listings_map = {}

        self.load_filters()
        self.load_listings_map()

    def load_listings_map(self):
        """Build mapping of location IDs to store names and cities."""
        self.listings_map = {}
        listings_file = self.csv_file.replace('_results.csv', '_total_listings.csv')
        listings_path = os.path.join(self.csv_folder, listings_file)
        if os.path.exists(listings_path):
            try:
                with open(listings_path, encoding='utf8') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    id_idx = header.index('id')
                    name_idx = header.index('name')
                    city_idx = header.index('city') if 'city' in header else -1
                    for row in reader:
                        if len(row) > max(id_idx, name_idx):
                            store_id = row[id_idx].strip()
                            store_name = row[name_idx].strip()
                            store_city = row[city_idx].strip() if city_idx >= 0 and len(row) > city_idx else ""
                            self.listings_map[store_id] = {
                                'name': store_name,
                                'city': store_city
                            }
                logger.info(f"Loaded {len(self.listings_map)} store names and cities from {listings_path}")
            except Exception as e:
                logger.warning(f"Failed to load listings map: {e}")

    def load_filters(self):
        """Load filters from flower-filters.json or create a default one."""
        if self.no_filter:
            # Create a single catch-all filter
            default_filter = FlowerFilter()
            default_filter.name = "All Results"
            default_filter.key = "prices.eighth"  # Default sort/price column
            self.filters = [default_filter]
            logger.info("No-filter mode enabled: Included all results.")
            return

        filters_path = os.path.join(
            os.path.dirname(__file__), 'flower-filters.json')
        try:
            with open(filters_path, 'r') as f:
                data = json.load(f)
                self.filters = [FlowerFilter(f_data)
                                for f_data in data.get('filters', [])]
            logger.info(
                f"Loaded {len(self.filters)} filters from {filters_path}")
        except Exception as e:
            logger.error(f"Failed to load filters: {str(e)}")

    def load_csv_data(self):
        """Read the CSV file and pre-filter rows with pricing data."""
        file_path = os.path.join(self.csv_folder, self.csv_file)

        # Fallback: If specific file not found, look for any result CSV in the folder
        if not os.path.exists(file_path):
            logger.warning(
                f"Primary CSV file not found: {file_path}. Searching for fallbacks...")
            fallback_pattern = os.path.join(self.csv_folder, "*_results.csv")
            fallbacks = glob.glob(fallback_pattern)
            if fallbacks:
                # Use the most recent fallback
                file_path = max(fallbacks, key=os.path.getmtime)
                logger.info(f"Using fallback CSV file: {file_path}")
            else:
                logger.error(f"No valid CSV data found in {self.csv_folder}")
                return False

        logger.info(f"Reading data from: {file_path}")
        try:
            with open(file_path, encoding="utf8") as f:
                reader = csv.reader(f)
                header = next(reader)
                self.header_map = {name.strip(): i for i, name in enumerate(header)}
                
                # Check for price fields dynamically
                price_price_idx = self.header_map.get('price.price', -1)
                prices_gram_idx = self.header_map.get('prices.gram', -1)
                prices_ounce_idx = self.header_map.get('prices.ounce', -1)
                
                self.raw_data = []
                for row in reader:
                    if not row or len(row) <= max(price_price_idx, prices_gram_idx, prices_ounce_idx):
                        continue
                    
                    # Row is valid if it has some non-zero numeric price or nested price JSON list
                    has_price = False
                    if price_price_idx >= 0:
                        val = row[price_price_idx]
                        if val and val != 'nan' and val.replace('.', '', 1).replace('-', '', 1).isdigit() and float(val) > 0:
                            has_price = True
                    if not has_price and prices_gram_idx >= 0:
                        val = row[prices_gram_idx]
                        if val and val != 'nan' and val != 'None' and '[' in val:
                            has_price = True
                    if not has_price and prices_ounce_idx >= 0:
                        val = row[prices_ounce_idx]
                        if val and val != 'nan' and val != 'None' and '[' in val:
                            has_price = True
                            
                    if has_price:
                        self.raw_data.append(row)
                        
            logger.info(f"Loaded {len(self.raw_data)} rows with pricing data.")
            return True
        except Exception as e:
            logger.error(f"Error reading CSV: {str(e)}")
            return False

    def apply_filters(self):
        """
        Iterate through all filters and apply them to the raw data.
        """
        if not self.raw_data:
            if not self.load_csv_data():
                return

        self.filtered_tables = []
        for f in self.filters:
            logger.info(f"Filtering for: {f.name}")

            # Identify the column key for the price (gram, eighth, etc.)
            price_col = f.key

            # Apply filters
            filtered: List[Any] = [
                # copy row to avoid mutating raw_data
                row[:] for row in self.raw_data
                if self.is_match(row, f, price_col)
            ]

            # Handle result limits and sorting
            if f.limit_results_amt > -1 and len(filtered) > f.limit_results_amt:
                filtered = sorted(filtered, key=lambda x: self.get_price_by_key(x, price_col) or 999999)
                filtered = filtered[:f.limit_results_amt]

            self.filtered_tables.append(filtered)
            logger.info(f"Filter '{f.name}' yielded {len(filtered)} results.")

    def get_col_by_key(self, key):
        """Legacy helper, returns key itself for dynamic routing."""
        return key

    def get_price_by_key(self, row, key):
        """
        Dynamically extract price for a key (e.g. 'prices.gram', 'prices.eighth') from the row.
        """
        # If the key is directly in header and contains a simple numeric value
        idx = self.header_map.get(key, -1)
        if idx >= 0 and idx < len(row):
            val = str(row[idx])
            if val and val != 'nan' and val.replace('.', '', 1).isdigit():
                return float(val)

        # Otherwise, parse the JSON fields ('prices.ounce', 'prices.gram')
        # Map filter key to the label we are searching for in the JSON price list
        label_mapping = {
            'prices.half_gram': ['half_gram', 'half gram', '1/2 g', '0.5 g', '0.5g', '1/2g'],
            'prices.gram': ['gram', '1 g', '1g', '1.0g', '1.0 g'],
            'prices.two_grams': ['two_grams', '2 g', '2g', '2.0g', '2.0 g'],
            'prices.eighth': ['eighth', '1/8', '3.5 g', '3.5g'],
            'prices.quarter': ['quarter', '1/4', '7 g', '7g', '7.0g'],
            'prices.half_ounce': ['half_ounce', 'half ounce', '1/2', '14 g', '14g'],
            'prices.ounce': ['ounce', '1 oz', '1oz', '28 g', '28g']
        }

        search_labels = label_mapping.get(key, [])
        
        # Check prices.ounce first (usually contains eighth, quarter, half, ounce)
        ounce_idx = self.header_map.get('prices.ounce', -1)
        if ounce_idx >= 0 and ounce_idx < len(row):
            ounce_val = row[ounce_idx]
            if ounce_val and ounce_val != 'nan' and ounce_val.startswith('['):
                try:
                    price_list = json.loads(ounce_val)
                    for item in price_list:
                        label = str(item.get('label', '')).lower()
                        units = str(item.get('units', '')).lower()
                        # If label matches any search label
                        if any(lbl in label or lbl in units for lbl in search_labels):
                            p = item.get('price')
                            if p is not None:
                                return float(p)
                except Exception:
                    pass

        # Check prices.gram next
        gram_idx = self.header_map.get('prices.gram', -1)
        if gram_idx >= 0 and gram_idx < len(row):
            gram_val = row[gram_idx]
            if gram_val and gram_val != 'nan' and gram_val.startswith('['):
                try:
                    price_list = json.loads(gram_val)
                    for item in price_list:
                        label = str(item.get('label', '')).lower()
                        units = str(item.get('units', '')).lower()
                        if any(lbl in label or lbl in units for lbl in search_labels):
                            p = item.get('price')
                            if p is not None:
                                return float(p)
                except Exception:
                    pass

        # Fallback: check price.price and price.unit
        price_price_idx = self.header_map.get('price.price', -1)
        price_unit_idx = self.header_map.get('price.unit', -1)
        price_quantity_idx = self.header_map.get('price.quantity', -1)
        if price_price_idx >= 0 and price_price_idx < len(row) and price_unit_idx >= 0 and price_unit_idx < len(row):
            unit_val = str(row[price_unit_idx]).lower()
            qty_val = str(row[price_quantity_idx]).lower() if price_quantity_idx >= 0 and price_quantity_idx < len(row) else ''
            
            # Map key to unit & quantity
            key_unit_qty = {
                'prices.half_gram': ('gram', '1/2'),
                'prices.gram': ('gram', '1'),
                'prices.eighth': ('ounce', '1/8'),
                'prices.quarter': ('ounce', '1/4'),
                'prices.half_ounce': ('ounce', '1/2'),
                'prices.ounce': ('ounce', '1')
            }
            if key in key_unit_qty:
                target_unit, target_qty = key_unit_qty[key]
                if target_unit in unit_val and (not target_qty or target_qty in qty_val or target_qty in unit_val):
                    p_val = row[price_price_idx]
                    if p_val and p_val != 'nan' and p_val.replace('.', '', 1).isdigit():
                        return float(p_val)
                        
            # If key is prices.gram and unit is unit (vapes/concentrates sold as a single unit)
            if key == 'prices.gram' and 'unit' in unit_val:
                p_val = row[price_price_idx]
                if p_val and p_val != 'nan' and p_val.replace('.', '', 1).isdigit():
                    return float(p_val)

        return None

    def is_match(self, row, f, price_col):
        """
        Check if a single CSV row matches the filter criteria.
        """
        # 1. Price Comparison
        if f.price:
            row_price = self.get_price_by_key(row, price_col)
            if row_price is None or not getComparisonVal(f.compare, row_price, f.price):
                return False

        # 2. Categories
        if f.categories:
            cat_idx = self.header_map.get('category.name', -1)
            cat_val = str(row[cat_idx]).lower() if cat_idx >= 0 and cat_idx < len(row) else ""
            if cat_val not in [c.lower() for c in f.categories]:
                return False

        # 3. Join row for word-based searches
        row_str = " ".join([str(x) for x in row]).lower()

        # 4. Brands
        if f.brands:
            if not any(brand.lower() in row_str for brand in f.brands):
                return False

        # 5. Strains
        if f.strains:
            if not any(strain.lower() in row_str for strain in f.strains):
                return False

        # 6. Stores
        if f.stores:
            loc_id = str(row[0]) if len(row) > 0 else ""
            dispensary_name = self.listings_map.get(loc_id, "").lower()
            if not any(store.lower() in dispensary_name for store in f.stores):
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
            thc_val = self.extract_thc(row)
            if thc_val < f.thc_floor:
                if f.thc_floor_strict:
                    return False

        # 10. CBD Floor
        if f.cbd_floor > 0.001:
            cbd_val = self.extract_cbd(row)
            if cbd_val < f.cbd_floor:
                if f.cbd_floor_strict:
                    return False

        return True

    def extract_thc(self, row):
        """Extract numeric value for THC from text or dedicated column."""
        thc_idx = self.header_map.get('metrics.aggregates.thc', -1)
        if thc_idx >= 0 and thc_idx < len(row):
            val = str(row[thc_idx])
            if val and val != 'nan' and val.replace('.', '', 1).isdigit():
                return float(val)
        return 0.0

    def extract_cbd(self, row):
        """Extract numeric value for CBD from text or dedicated column."""
        cbd_idx = self.header_map.get('metrics.aggregates.cbd', -1)
        if cbd_idx >= 0 and cbd_idx < len(row):
            val = str(row[cbd_idx])
            if val and val != 'nan' and val.replace('.', '', 1).isdigit():
                return float(val)
        return 0.0

    def clean_html(self, raw_html):
        """Remove HTML tags from a string."""
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', str(raw_html))

    def as_currency(self, amount):
        """Format number as USD currency."""
        try:
            return '${:,.2f}'.format(float(amount))
        except Exception:
            return str(amount)

    def as_percentage(self, amount):
        """Format number as percentage."""
        try:
            val = float(amount)
            if 0 <= val <= 100:
                return '{:,.2f}%'.format(val)
        except Exception:
            pass
        return ""

    def generate_html(self):
        """Build the full HTML dashboard."""
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html', lang="en"):
            with tag('head'):
                self._add_html_head(doc)
            with tag('body'):
                doc.asis('<a href="#main-content" class="skip-link">Skip to main content</a>')
                with tag('div', klass="container-fluid main", id="main-content", tabindex="-1"):
                    self._generate_navbar(doc, tag, text)
                    # Global Search Bar
                    with tag('div', klass="search-container"):
                        doc.stag('input', ('aria-label', 'Search products, brands, categories, or dispensaries'), type="text", id="global-search",
                                 placeholder="🔍 Search products, brands, categories, or dispensaries...", 
                                 klass="search-input")
                    for i, f in enumerate(self.filters):
                        self._generate_filter_section(doc, tag, text, i, f)
                    self._generate_footer(doc, tag, text)

        raw_html = doc.getvalue()
        if len(raw_html) < 5 * 1024 * 1024:
            try:
                return indent(raw_html)
            except Exception:
                pass
        return raw_html

    def _is_valid_url(self, url: str) -> bool:
        if not url:
            return False
        url_str = str(url).strip()
        return url_str.startswith(('http://', 'https://', '#', '/'))

    def _add_html_head(self, doc):
        """Append metadata and script links to head."""
        doc.asis('<meta charset="utf-8">')
        doc.asis(
            '<meta name="viewport" content="width=device-width, initial-scale=1">')
        doc.asis('<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\' https: data:; style-src \'self\' \'unsafe-inline\' https://fonts.googleapis.com https://cdn.jsdelivr.net; font-src https://fonts.gstatic.com; script-src \'self\' \'unsafe-inline\' https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com;">')
        doc.asis('<link rel="preconnect" href="https://fonts.googleapis.com">')
        doc.asis(
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
        doc.asis('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">')
        doc.asis('<link href="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.css" rel="stylesheet">')

        # Premium Glassmorphism CSS
        css = """
        :root {
            --primary: #00ffa3;
            --secondary: #00d4ff;
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #f59e0b;
            --glass: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Outfit', 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(0, 255, 163, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(0, 212, 255, 0.05) 0%, transparent 40%);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }

        .skip-link {
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--primary);
            color: var(--bg);
            padding: 8px;
            z-index: 100;
            transition: top 0.2s ease;
            font-weight: 600;
            text-decoration: none;
            border-radius: 0 0 8px 0;
        }

        .skip-link:focus {
            top: 0;
            outline: none;
        }

        *:focus-visible {
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }

        /* Navbar / Header */
        .navbar {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 1.5rem 2rem;
            margin-bottom: 3rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .navbar-brand {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .navbar-nav {
            display: flex;
            gap: 1.5rem;
            list-style: none;
        }

        .nav-link {
            color: var(--text);
            text-decoration: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 12px;
            transition: all 0.2s;
        }

        .nav-link:hover {
            background: rgba(0, 255, 163, 0.1);
            color: var(--primary);
        }

        /* Section Headers */
        h3 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .badge {
            background: var(--primary);
            color: var(--bg);
            padding: 0.25rem 0.75rem;
            border-radius: 100px;
            font-size: 0.9rem;
            font-weight: 800;
        }

        /* Table Styles */
        .table-container {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 3rem;
            overflow-x: auto;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            color: var(--text);
        }
        
        th {
            text-align: left;
            padding: 1rem;
            color: var(--primary);
            font-weight: 600;
            border-bottom: 1px solid var(--glass-border);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.85rem;
            white-space: nowrap;
        }
        
        td {
            padding: 1rem;
            border-bottom: 1px solid var(--glass-border);
            vertical-align: middle;
        }
        
        tr:last-child td { border-bottom: none; }
        
        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
            transition: background 0.2s;
        }
        
        .price-tag {
            font-weight: 700;
            color: var(--accent);
            font-family: monospace;
            font-size: 1.1rem;
        }
        
        .img-thumbnail {
            width: 60px;
            height: 60px;
            border-radius: 12px;
            object-fit: cover;
            border: 2px solid var(--glass-border);
            background: var(--glass);
            transition: transform 0.2s, border-color 0.2s;
        }
        
        .img-thumbnail:hover {
            transform: scale(1.1);
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(0, 255, 163, 0.3);
        }
        
        a {
            color: var(--secondary);
            text-decoration: none;
            transition: color 0.2s;
        }
        
        a:hover {
            color: var(--primary);
            text-shadow: 0 0 8px rgba(0, 255, 163, 0.4);
        }

        .info-cell {
            font-size: 0.9rem;
            color: var(--text-muted);
            max-width: 300px;
        }

        /* Responsive Table */
        @media (max-width: 768px) {
            body { padding: 1rem; }
            .navbar {
                flex-direction: column;
                gap: 1rem;
                padding: 1.5rem;
                text-align: center;
            }
            .navbar-nav {
                flex-wrap: wrap;
                justify-content: center;
            }
            h3 { font-size: 1.5rem; }
            
            .table-container {
                padding: 0.5rem;
                border: none;
                background: transparent;
                box-shadow: none;
            }
            
            table, thead, tbody, th, td, tr {
                display: block;
            }
            
            thead {
                display: none;
            }
            
            tr {
                background: var(--card-bg);
                backdrop-filter: blur(12px);
                border: 1px solid var(--glass-border);
                border-radius: 16px;
                margin-bottom: 1.5rem;
                padding: 1rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            td {
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                padding: 0.75rem 0.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                text-align: right;
            }
            
            td:last-child {
                border-bottom: none;
            }
            
            td::before {
                content: attr(data-label);
                font-weight: 600;
                color: var(--primary);
                text-transform: uppercase;
                font-size: 0.8rem;
                letter-spacing: 0.05em;
                margin-right: 1rem;
                text-align: left;
            }
            
            .info-cell {
                max-width: 100%;
                text-align: right;
            }
        }

        .footer {
            text-align: center;
            color: var(--text-muted);
            padding: 2rem;
            margin-top: 4rem;
            border-top: 1px solid var(--glass-border);
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: var(--card-bg); border-radius: 5px; border: 1px solid var(--glass-border); }
        ::-webkit-scrollbar-thumb:hover { background: var(--glass-border); }

        /* Modern Search Input styling */
        .search-container {
            margin-bottom: 2rem;
            display: flex;
            justify-content: center;
            width: 100%;
        }

        .search-input {
            width: 100%;
            max-width: 600px;
            padding: 1rem 1.5rem;
            border-radius: 100px;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            color: var(--text);
            font-family: inherit;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(0, 255, 163, 0.3);
            transform: scale(1.02);
        }
        """

        with doc.tag('style'):
            doc.asis(css)

        # Scripts
        doc.asis(
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>')
        doc.asis(
            '<script src="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"></script>')

        js_code = """
        $(document).ready(function() {
            var sections = {};
            var activeFilters = {};
            var activeSort = {};
            var pageSize = 50;
            var currentPages = {};

            // Parse data from script tags
            $('script[id^="data-"]').each(function() {
                var id = $(this).attr('id').replace('data-', '');
                try {
                    sections[id] = JSON.parse($(this).html());
                    currentPages[id] = 1;
                    activeFilters[id] = "";
                    activeSort[id] = { index: null, order: 'asc' };
                } catch(e) {
                    console.error("Failed to parse data for section " + id, e);
                }
            });

            // Currency formatter
            function asCurrency(val) {
                if (val === null || val === undefined || isNaN(val)) return "-";
                return "$" + parseFloat(val).toFixed(2);
            }

            // Percentage formatter
            function asPercentage(val) {
                if (!val) return "-";
                return parseFloat(val).toFixed(2) + "%";
            }

            // Render a single row
            function buildRow(item) {
                var tr = $('<tr></tr>');
                
                // Price
                var priceTag = $('<div class="price-tag"></div>').text(asCurrency(item.price));
                tr.append($('<td data-label="Price"></td>').append(priceTag));
                
                // Image
                var imgTd = $('<td class="thumb" data-label="Image"></td>');
                if (item.img_url && item.img_url !== "None" && item.img_url !== "nan") {
                    var a = $('<a data-fancybox="gallery"></a>').attr('href', item.img_url).attr('aria-label', "View full image of " + (item.name || 'product'));
                    var img = $('<img class="img-thumbnail">')
                        .attr('src', item.img_url)
                        .attr('alt', item.name || 'product')
                        .on('error', function() { this.src = "https://images.weedmaps.com/static/avatar/dispensary.png"; });
                    imgTd.append(a.append(img));
                } else {
                    imgTd.text("-");
                }
                tr.append(imgTd);
                
                // Product Name & Brand
                var prodTd = $('<td data-label="Product"></td>');
                var prodLink = $('<a target="_blank" style="font-weight: 600; display: block; margin-bottom: 4px;"></a>')
                    .attr('href', item.url || '#').text(item.name || 'N/A');
                prodTd.append(prodLink);
                if (item.brand) {
                    var brandSpan = $('<span style="font-size: 0.8rem; color: var(--text-muted);"></span>').text(item.brand);
                    prodTd.append(brandSpan);
                }
                tr.append(prodTd);
                
                // Category
                var catSpan = $('<span style="background: rgba(0, 212, 255, 0.1); color: var(--secondary); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;"></span>').text(item.category);
                tr.append($('<td data-label="Category"></td>').append(catSpan));
                
                // THC
                tr.append($('<td data-label="THC"></td>').text(asPercentage(item.thc)));
                
                // CBD
                if (item.cbd !== undefined && item.cbd !== null) {
                    tr.append($('<td data-label="CBD"></td>').text(asPercentage(item.cbd)));
                }
                
                // Dispensary
                tr.append($('<td data-label="Dispensary"></td>').text(item.dispensary || "N/A"));
                
                // City
                tr.append($('<td data-label="City"></td>').text(item.city || "N/A"));
                
                // Details
                var desc = item.desc || "";
                if (desc.length > 100) desc = desc.substring(0, 100) + "...";
                tr.append($('<td class="info-cell" data-label="Details"></td>').text(desc));
                
                return tr;
            }

            // Filter and Sort helper
            function getProcessedData(sectionId) {
                var data = sections[sectionId] || [];
                
                // Apply filter
                var query = activeFilters[sectionId].toLowerCase();
                if (query) {
                    data = data.filter(function(item) {
                        return (item.name && item.name.toLowerCase().indexOf(query) > -1) ||
                               (item.brand && item.brand.toLowerCase().indexOf(query) > -1) ||
                               (item.category && item.category.toLowerCase().indexOf(query) > -1) ||
                               (item.dispensary && item.dispensary.toLowerCase().indexOf(query) > -1) ||
                               (item.city && item.city.toLowerCase().indexOf(query) > -1) ||
                               (item.desc && item.desc.toLowerCase().indexOf(query) > -1);
                    });
                }
                
                // Apply sort
                var sort = activeSort[sectionId];
                if (sort && sort.index !== null) {
                    data.sort(function(a, b) {
                        var valA = getSortValue(a, sort.index);
                        var valB = getSortValue(b, sort.index);
                        if (typeof valA === 'number' && typeof valB === 'number') {
                            return sort.order === 'asc' ? valA - valB : valB - valA;
                        }
                        return sort.order === 'asc' ? String(valA).localeCompare(String(valB)) : String(valB).localeCompare(String(valA));
                    });
                }
                
                return data;
            }

            function getSortValue(item, headerIndex) {
                var hasCbd = item.cbd !== undefined && item.cbd !== null;
                var mapping = [];
                if (hasCbd) {
                    mapping = ['price', null, 'name', 'category', 'thc', 'cbd', 'dispensary', 'city', 'desc'];
                } else {
                    mapping = ['price', null, 'name', 'category', 'thc', 'dispensary', 'city', 'desc'];
                }
                var prop = mapping[headerIndex];
                if (!prop) return "";
                var val = item[prop];
                if (prop === 'price' || prop === 'thc' || prop === 'cbd') {
                    return parseFloat(val) || 0;
                }
                return val ? val.toLowerCase() : "";
            }

            // Render table content for a section
            function renderSection(id) {
                var container = $(document.getElementById(id));
                var tbody = container.find('tbody');
                tbody.empty();
                
                var data = getProcessedData(id);
                
                // Update badge
                container.find('h3 .badge').text(data.length);
                
                var totalRows = data.length;
                
                // Handle empty state
                if (totalRows === 0) {
                    container.find('.table-container').hide();
                    if (container.find('.no-match-msg').length === 0) {
                        container.append('<p class="no-match-msg" style="color: var(--text-muted); padding: 1rem;">No matching items found in this section.</p>');
                    } else {
                        container.find('.no-match-msg').show();
                    }
                    container.find('.pagination-controls').remove();
                    return;
                }
                
                container.find('.table-container').show();
                container.find('.no-match-msg').hide();
                
                // Paginate
                var page = currentPages[id] || 1;
                var totalPages = Math.ceil(totalRows / pageSize);
                if (page > totalPages) page = totalPages || 1;
                currentPages[id] = page;
                
                var start = (page - 1) * pageSize;
                var end = start + pageSize;
                var pageData = data.slice(start, end);
                
                // Render rows
                $.each(pageData, function(idx, item) {
                    tbody.append(buildRow(item));
                });
                
                // Render pagination controls
                container.find('.pagination-controls').remove();
                if (totalRows > pageSize) {
                    var controls = $('<div class="pagination-controls" style="margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); padding: 1rem; border-radius: 12px; border: 1px solid var(--glass-border);"></div>');
                    var prevBtn = $('<button class="btn btn-secondary" style="background: var(--glass); border: 1px solid var(--glass-border); color: var(--text); padding: 0.5rem 1.2rem; border-radius: 8px; cursor: pointer; transition: all 0.2s;">Previous</button>');
                    var nextBtn = $('<button class="btn btn-secondary" style="background: var(--glass); border: 1px solid var(--glass-border); color: var(--text); padding: 0.5rem 1.2rem; border-radius: 8px; cursor: pointer; transition: all 0.2s;">Next</button>');
                    var info = $('<span style="color: var(--text-muted); font-size: 0.9rem;">Showing ' + (start + 1) + '-' + Math.min(end, totalRows) + ' of ' + totalRows + '</span>');
                    
                    if (page === 1) prevBtn.prop('disabled', true).css('opacity', 0.5);
                    if (page === totalPages) nextBtn.prop('disabled', true).css('opacity', 0.5);
                    
                    prevBtn.on('click', function() {
                        currentPages[id]--;
                        renderSection(id);
                    });
                    nextBtn.on('click', function() {
                        currentPages[id]++;
                        renderSection(id);
                    });
                    
                    controls.append(prevBtn).append(info).append(nextBtn);
                    container.find('.table-container').after(controls);
                }
            }

            // Setup sorting indicators and events
            $('th').each(function() {
                var text = $(this).text().trim();
                if (text && text !== 'IMAGE' && text !== 'DETAILS') {
                    $(this).css('cursor', 'pointer').append(' <span class="sort-icon" style="color: var(--text-muted); font-size: 0.8rem; margin-left: 4px;">↕</span>');
                }
            });

            $('th').on('click', function() {
                var text = $(this).text().trim();
                if (text === 'IMAGE' || text === 'DETAILS') return;
                
                var table = $(this).closest('table');
                var sectionId = $(this).closest('div[id]').attr('id');
                var index = $(this).index();
                
                var sort = activeSort[sectionId];
                var order = 'asc';
                if (sort.index === index) {
                    order = sort.order === 'asc' ? 'desc' : 'asc';
                }
                
                activeSort[sectionId] = { index: index, order: order };
                
                // Update icons in table headers
                table.find('th .sort-icon').html('↕').css('color', 'var(--text-muted)');
                $(this).find('.sort-icon').html(order === 'asc' ? '▲' : '▼').css('color', 'var(--primary)');
                
                // Reset page to 1 on sort change
                currentPages[sectionId] = 1;
                renderSection(sectionId);
            });

            // Global search
            $('#global-search').on('keyup', function() {
                var val = $(this).val();
                $.each(sections, function(id, data) {
                    activeFilters[id] = val;
                    currentPages[id] = 1; // Reset to page 1
                    renderSection(id);
                });
            });

            // Initial render of all sections
            $.each(sections, function(id, data) {
                renderSection(id);
            });
        });
        """
        doc.asis(f'<script>{js_code}</script>')

    def _generate_navbar(self, doc, tag, text):
        """Generate common navigation bar."""
        with tag('nav', klass="navbar"):
            with tag('div', klass="navbar-brand"):
                text("CANADATA ANALYTICS")

            with tag('div'):
                with tag('ul', klass="navbar-nav"):
                    for f in self.filters:
                        with tag('li'):
                            with tag('a', klass="nav-link", href=f'#{f.name.replace(" ", "_").lower()}'):
                                text(f.name)

            with tag('div', style="text-align: right"):
                with tag('div', style="font-size: 0.8rem; color: var(--text-muted)"):
                    text(f"Source: {self.csv_file}")
                with tag('div', style="font-size: 0.8rem; color: var(--accent)"):
                    now = datetime.now().strftime("%b %d, %Y")
                    text(f"Updated: {now}")

    def _generate_filter_section(self, doc, tag, text, i, f):
        """Generate a table for a specific filter."""
        results = self.filtered_tables[i]
        section_id = f.name.replace(" ", "_").lower()

        with tag('div', id=section_id):
            with tag('h3'):
                text(f.name)
                with tag('span', klass="badge"):
                    text(str(len(results)))

            if not results:
                with tag('p', style="color: var(--text-muted); padding: 1rem;"):
                    text("No results found for this filter.")
                return

            # Write data to a script block for performant client-side rendering
            img_idx = self.header_map.get('avatar_image.original_url', -1)
            name_idx = self.header_map.get('name', -1)
            brand_idx = self.header_map.get('brand_endorsement.brand_name', -1)
            slug_idx = self.header_map.get('slug', -1)
            cat_idx = self.header_map.get('category.name', -1)
            loc_idx = self.header_map.get('locations_found_at', -1)
            desc_idx = self.header_map.get('catalog_slug', -1)
            price_col = f.key

            serialized_rows = []
            for row in results:
                img_url = str(row[img_idx]) if img_idx >= 0 and img_idx < len(row) else ""
                prod_name = str(row[name_idx]) if name_idx >= 0 and name_idx < len(row) else "N/A"
                brand_name = str(row[brand_idx]) if brand_idx >= 0 and brand_idx < len(row) else ""
                slug_val = str(row[slug_idx]) if slug_idx >= 0 and slug_idx < len(row) else ""
                category_name = str(row[cat_idx]) if cat_idx >= 0 and cat_idx < len(row) else ""
                p_val = self.get_price_by_key(row, price_col)
                thc_val = self.extract_thc(row)
                cbd_val = self.extract_cbd(row) if f.cbd_floor > 0 else None
                
                loc_id = str(row[0]) if len(row) > 0 else ""
                store_info = self.listings_map.get(loc_id, {})
                dispensary_name = store_info.get('name', "") if isinstance(store_info, dict) else store_info
                if not dispensary_name:
                    if loc_idx >= 0 and len(row) > loc_idx:
                        loc_val = row[loc_idx]
                        if '/' in loc_val:
                            dispensary_name = loc_val.split('/')[-1].replace('"', '').replace(']', '').replace('-', ' ').title()
                
                store_city = store_info.get('city', "") if isinstance(store_info, dict) else ""
                
                desc = self.clean_html(row[desc_idx]) if desc_idx >= 0 and desc_idx < len(row) else ""
                if desc == "None" or desc == "nan":
                    desc = ""
                
                loc_val = ""
                if loc_idx >= 0 and loc_idx < len(row):
                    loc_raw = str(row[loc_idx])
                    if '[' in loc_raw:
                        try:
                            loc_list = json.loads(loc_raw)
                            if loc_list:
                                loc_val = str(loc_list[0])
                        except Exception:
                            loc_val = loc_raw.replace('[', '').replace(']', '').replace('"', '').replace("'", "").strip()
                    else:
                        loc_val = loc_raw.strip()

                if loc_val and slug_val:
                    loc_val_clean = loc_val.rstrip('/')
                    url = f"https://weedmaps.com{loc_val_clean}/menu/{slug_val}"
                else:
                    url = "#"

                serialized_rows.append({
                    'price': p_val,
                    'img_url': img_url,
                    'name': prod_name,
                    'brand': brand_name,
                    'category': category_name,
                    'thc': thc_val,
                    'cbd': cbd_val,
                    'dispensary': dispensary_name,
                    'city': store_city,
                    'desc': desc,
                    'url': url
                })

            with tag('script', id=f"data-{section_id}", type="application/json"):
                # Prevent XSS by escaping characters that can break out of the script tag
                safe_json = json.dumps(serialized_rows).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
                doc.asis(safe_json)

            with tag('div', klass='table-container'):
                with tag('table'):
                    with tag('thead'):
                        with tag('tr'):
                            # Define headers based on data content
                            headers = ['Price', 'Image',
                                       'Product', 'Category', 'THC']
                            if f.cbd_floor > 0:
                                headers.append('CBD')
                            headers.extend(['Dispensary', 'City', 'Details'])

                            for label in headers:
                                with tag('th'):
                                    text(label)

                    with tag('tbody'):
                        pass

    def _generate_row(self, doc, tag, text, row, f):
        """Generate a single table row."""
        price_col = f.key
        
        # Get dynamic indices
        img_idx = self.header_map.get('avatar_image.original_url', -1)
        name_idx = self.header_map.get('name', -1)
        brand_idx = self.header_map.get('brand_endorsement.brand_name', -1)
        slug_idx = self.header_map.get('slug', -1)
        cat_idx = self.header_map.get('category.name', -1)
        
        # Resolve values
        img_url = str(row[img_idx]) if img_idx >= 0 and img_idx < len(row) else ""
        prod_name = str(row[name_idx]) if name_idx >= 0 and name_idx < len(row) else "N/A"
        brand_name = str(row[brand_idx]) if brand_idx >= 0 and brand_idx < len(row) else ""
        if brand_name == "None":
            brand_name = ""
        slug_val = str(row[slug_idx]) if slug_idx >= 0 and slug_idx < len(row) else ""
        category_name = str(row[cat_idx]) if cat_idx >= 0 and cat_idx < len(row) else ""
        
        # Resolve Weedmaps product page URL from locations_found_at
        loc_idx = self.header_map.get('locations_found_at', -1)
        loc_val = ""
        if loc_idx >= 0 and loc_idx < len(row):
            loc_raw = str(row[loc_idx])
            if '[' in loc_raw:
                try:
                    loc_list = json.loads(loc_raw)
                    if loc_list:
                        loc_val = str(loc_list[0])
                except Exception:
                    loc_val = loc_raw.replace('[', '').replace(']', '').replace('"', '').replace("'", "").strip()
            else:
                loc_val = loc_raw.strip()

        if loc_val and slug_val:
            loc_val_clean = loc_val.rstrip('/')
            url = f"https://weedmaps.com{loc_val_clean}/menu/{slug_val}"
        else:
            url = "#"
            
        with tag('tr'):
            # Price
            with tag('td'):
                with tag('div', klass="price-tag"):
                    p_val = self.get_price_by_key(row, price_col)
                    text(self.as_currency(p_val) if p_val is not None else "-")

            # Image
            with tag('td', klass="thumb"):
                if img_url and img_url != "None" and img_url != "nan":
                    safe_img_url = img_url if self._is_valid_url(img_url) else 'https://images.weedmaps.com/static/avatar/dispensary.png'
                    with tag('a', ('data-fancybox', 'gallery'), ('aria-label', f"View full image of {prod_name}"), href=safe_img_url):
                        doc.stag('img', src=safe_img_url, alt=prod_name, klass="img-thumbnail",
                                 onerror="this.src='https://images.weedmaps.com/static/avatar/dispensary.png';")
                else:
                    text("-")

            # Strain Name + Link
            with tag('td'):
                safe_url = url if self._is_valid_url(url) else '#'
                with tag('a', href=safe_url, target="_blank", style="font-weight: 600; display: block; margin-bottom: 4px;"):
                    text(prod_name)
                if brand_name:
                    with tag('span', style="font-size: 0.8rem; color: var(--text-muted);"):
                        text(brand_name)

            # Category
            with tag('td'):
                with tag('span', style="background: rgba(0, 212, 255, 0.1); color: var(--secondary); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;"):
                    text(category_name)

            # THC
            thc_val = self.extract_thc(row)
            with tag('td'):
                text(self.as_percentage(thc_val) if thc_val else "-")

            # CBD
            if f.cbd_floor > 0:
                cbd_val = self.extract_cbd(row)
                with tag('td'):
                    text(self.as_percentage(cbd_val) if cbd_val else "-")

            # Dispensary
            with tag('td'):
                loc_id = str(row[0]) if len(row) > 0 else ""
                store_info = self.listings_map.get(loc_id, {})
                dispensary_name = store_info.get('name', "") if isinstance(store_info, dict) else store_info
                if not dispensary_name:
                    loc_idx = self.header_map.get('locations_found_at', -1)
                    if loc_idx >= 0 and len(row) > loc_idx:
                        loc_val = row[loc_idx]
                        if '/' in loc_val:
                            dispensary_name = loc_val.split('/')[-1].replace('"', '').replace(']', '').replace('-', ' ').title()
                text(dispensary_name or "N/A")

            # City
            with tag('td'):
                loc_id = str(row[0]) if len(row) > 0 else ""
                store_info = self.listings_map.get(loc_id, {})
                store_city = store_info.get('city', "") if isinstance(store_info, dict) else ""
                text(store_city or "N/A")

            # Info (Cleaned)
            with tag('td', klass="info-cell"):
                # Use catalog_slug as info fallback if desc is empty
                desc_idx = self.header_map.get('catalog_slug', -1)
                desc = self.clean_html(row[desc_idx]) if desc_idx >= 0 and desc_idx < len(row) else ""
                if desc == "None" or desc == "nan":
                    desc = ""
                # Truncate if too long
                if len(desc) > 100:
                    desc = desc[:100] + "..."
                text(desc)

    def _generate_footer(self, doc, tag, text):
        """Add footer boilerplate."""
        with tag('div', klass="footer"):
            text("© 2026 CanaData Analytics • Generated with ❤️ and ☕")

    def save_html(self, output_path="output/index.html"):
        """Save generated HTML to file."""
        html_content = self.generate_html()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"HTML report saved to: {output_path}")


def getComparisonVal(op, val1, val2):
    """Evaluate a comparison operation."""
    try:
        if op == '>=':
            return 1 if val1 >= val2 else 0
        if op == '<=':
            return 1 if 0 < val1 <= val2 else 0
        if op == '==':
            return 1 if val1 == val2 else 0
        if op == '>':
            return 1 if val1 > val2 else 0
        if op == '<':
            return 1 if 0 < val1 < val2 else 0
    except Exception:
        pass
    return 0


def main():
    """Execution entry point."""
    parser_args = argparse.ArgumentParser(
        description="CanaParse: Filter and generate HTML reports from CanaData CSVs.")
    parser_args.add_argument(
        "--file", help="Specific CSV file name (e.g., results.csv)")
    parser_args.add_argument(
        "--folder", help="Specific folder containing the CSV file")
    parser_args.add_argument(
        "--output", default="output/index.html", help="Path to save the HTML report")
    parser_args.add_argument(
        "--no-filter", action="store_true", help="Include all results without filtering")

    args = parser_args.parse_args()

    parser = CanaParse(csv_file=args.file,
                       csv_folder=args.folder, no_filter=args.no_filter)
    if parser.load_csv_data():
        parser.apply_filters()
        parser.save_html(output_path=args.output)
    else:
        logger.error("Skipping report generation due to missing data.")


if __name__ == "__main__":
    main()
