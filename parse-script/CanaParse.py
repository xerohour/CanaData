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

        self.load_filters()

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
                # Skip rows that don't have at least one numeric price column (indices 9-15)
                self.raw_data = [
                    row for row in reader
                    if len(row) > 15 and any(
                        str(row[i]).replace(
                            '.', '', 1).isdigit() and float(row[i]) > 0
                        for i in range(9, 16)
                    )
                ]
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

            # Identify the column index for the price key (gram, eighth, etc.)
            price_col = self.get_col_by_key(f.key)

            # Apply filters
            filtered: List[Any] = [
                # copy row to avoid mutating raw_data
                row[:] for row in self.raw_data
                if self.is_match(row, f, price_col)
            ]

            # Handle result limits and sorting
            if f.limit_results_amt > -1 and len(filtered) > f.limit_results_amt:
                filtered = sorted(filtered, key=lambda x: float(str(x[price_col])) if str(
                    x[price_col]).replace('.', '', 1).isdigit() else 999999)
                filtered = filtered[:f.limit_results_amt]

            self.filtered_tables.append(filtered)
            logger.info(f"Filter '{f.name}' yielded {len(filtered)} results.")

    def get_col_by_key(self, key):
        """Map price keys to CSV column indices."""
        mapping = {
            'prices.gram': 9,
            'prices.two_grams': 10,
            'prices.eighth': 11,
            'prices.quarter': 12,
            'prices.half_ounce': 13,
            'prices.ounce': 14,
            'prices.half_gram': 15
        }
        return mapping.get(key, 9)

    def is_match(self, row, f, price_col):
        """
        Check if a single CSV row matches the filter criteria.
        """
        # 1. Price Comparison
        if f.price:
            row_price_raw = str(row[price_col])
            row_price = float(row_price_raw) if row_price_raw.replace(
                '.', '', 1).isdigit() else 0
            if not getComparisonVal(f.compare, row_price, f.price):
                return False

        # 2. Categories (Index 20)
        if f.categories:
            if str(row[20]).lower() not in [c.lower() for c in f.categories]:
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
                if f.thc_floor_strict:
                    return False
            else:
                row.append(f"thc+{thc_val}")

        # 10. CBD Floor
        if f.cbd_floor > 0.001:
            cbd_val = self.extract_cannabinoid(row_str, 'cbd')
            if cbd_val < f.cbd_floor:
                if f.cbd_floor_strict:
                    return False
            else:
                row.append(f"cbd+{cbd_val}")

        return True

    def extract_cannabinoid(self, text, type_name):
        """Extract numeric value for THC or CBD from text."""
        pattern = rf"{type_name}[:\s-]*(\d+\.?\d*)"
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1))
            except Exception:
                pass
        return 0

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

    def clean_html(self, raw_html):
        """Remove HTML tags from a string."""
        cleanr = re.compile('<.*?>')
        return re.sub(cleanr, '', str(raw_html))

    def generate_html(self):
        """Build the full HTML dashboard."""
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html', lang="en"):
            with tag('head'):
                self._add_html_head(doc)
            with tag('body'):
                with tag('div', klass="container-fluid main"):
                    self._generate_navbar(doc, tag, text)
                    for i, f in enumerate(self.filters):
                        self._generate_filter_section(doc, tag, text, i, f)
                    self._generate_footer(doc, tag, text)

        return indent(doc.getvalue())

    def _add_html_head(self, doc):
        """Append metadata and script links to head."""
        doc.asis('<meta charset="utf-8">')
        doc.asis(
            '<meta name="viewport" content="width=device-width, initial-scale=1">')
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
        """

        with doc.tag('style'):
            doc.asis(css)

        # Scripts
        doc.asis(
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>')
        doc.asis(
            '<script src="https://cdn.jsdelivr.net/gh/fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"></script>')
        # Note: Sorting script removed for now as it relied on old jquery tablesorter.
        # Could re-add a modern vanilla JS sorter later.

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

            with tag('div', klass='table-container'):
                with tag('table'):
                    with tag('thead'):
                        with tag('tr'):
                            # Define headers based on data content
                            headers = ['Price', 'Image',
                                       'Product', 'Category', 'THC']
                            if f.cbd_floor > 0:
                                headers.append('CBD')
                            headers.extend(['Dispensary', 'Details'])

                            for label in headers:
                                with tag('th'):
                                    text(label)

                    with tag('tbody'):
                        for row in results:
                            self._generate_row(doc, tag, text, row, f)

    def _generate_row(self, doc, tag, text, row, f):
        """Generate a single table row."""
        price_col = self.get_col_by_key(f.key)
        with tag('tr'):
            # Price
            with tag('td'):
                with tag('div', klass="price-tag"):
                    text(self.as_currency(row[price_col]))

            # Image
            with tag('td', klass="thumb"):
                img_url = str(row[17]) if len(row) > 17 else ""
                if img_url:
                    with tag('a', ('data-fancybox', 'gallery'), href=img_url):
                        doc.stag('img', src=img_url, klass="img-thumbnail",
                                 onerror="this.src='https://images.weedmaps.com/static/avatar/dispensary.png';")
                else:
                    text("-")

            # Strain Name + Link
            with tag('td'):
                slug = str(row[28]) if len(row) > 28 else ""
                url = f'https://weedmaps.com{slug.replace("#", "")}'
                with tag('a', href=url, target="_blank", style="font-weight: 600; display: block; margin-bottom: 4px;"):
                    text(str(row[2]))
                # Brand (assumed index 4 based on typical CSV layout, checking correctness)
                # Actually index 4 is usually brand in CanaData export
                brand = str(row[4]) if len(row) > 4 else ""
                if brand:
                    with tag('span', style="font-size: 0.8rem; color: var(--text-muted);"):
                        text(brand)

            # Category
            with tag('td'):
                with tag('span', style="background: rgba(0, 212, 255, 0.1); color: var(--secondary); padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;"):
                    text(str(row[20]))

            # THC
            thc_val = next(
                (str(s).split("+")[1] for s in row if str(s).startswith("thc+")), "0")
            with tag('td'):
                text(self.as_percentage(thc_val))

            # CBD
            if f.cbd_floor > 0:
                cbd_val = next(
                    (str(s).split("+")[1] for s in row if str(s).startswith("cbd+")), "0")
                with tag('td'):
                    text(self.as_percentage(cbd_val))

            # Dispensary
            with tag('td'):
                text(str(row[29]))

            # Info (Cleaned)
            with tag('td', klass="info-cell"):
                desc = self.clean_html(row[1])
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
