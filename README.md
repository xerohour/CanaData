# CanaData 🌿

**Retrieve comprehensive cannabis listing and menu data from Weedmaps with ease.**

---

## 🚀 Overview

CanaData is a powerful Python-based scraper designed to help consumers and researchers understand the cannabis market. By extracting data from Weedmaps, it allows you to compare prices, product availability, and service types across different dispensaries and deliveries in any US state or specific city.

### 💡 Why CanaData?
Prices for the same product can vary significantly between locations. CanaData helps you find the best deals and puts retailers in competition, ensuring you don't overpay for your medicine or recreational products.

---

## 🛠️ Installation

1. **Python 3**: Ensure you have Python 3 installed. [Download it here](https://www.python.org/downloads/).
2. **Clone/Download**: Download this repository or clone it to your local machine.
3. **Dependencies**: Open your terminal/command prompt and install the required library:
   ```bash
   pip install requests
   ```

---

## 📖 Usage

Navigate to the project folder in your terminal and run:

```bash
python CanaData.py
```

### Options when prompted:
- **City/State Slug**: Enter a location (e.g., `los-angeles`, `colorado`).
- **`all`**: Will loop through a predefined list of all 50 states (Warning: Large states like California take significant time!).
- **`mylist`**: Reads from a local `mylist.txt` file (one slug per line).
- **`slugs`**: Reads from a local `slugs.txt` file.

### Advanced Usage (Command Line Arguments):
- `-go [slug]`: Quickstart the script with a specific slug or keyword (`all`, `mylist`).
- `-tshoot`: Enable troubleshooting mode for more verbose output.

---

## 📂 Output

Results are saved in a timestamped folder (e.g., `CanaData_02-17-2026/`):
- **`[slug]_results.csv`**: Every menu item with flattened attributes (Price, THC%, etc).
- **`[slug]_total_listings.csv`**: Metadata for every location found in the area.

---

## 🧠 Technical Details

For a deep dive into the scraping logic, data flattening algorithm, and class structure, check out the:
👉 **[Architecture & Logic Documentation](./DOCUMENTATION.md)**

---

## 💬 Community & Support

Join our Discord to discuss the project, request features, or report issues:
[**Join the Discord**](https://discord.gg/6WAcVek)

## 🌟 New Features

- **Logging System**: Improved visibility into the scraping process with timestamps and severity levels.
- **Environment Configuration**: Configure your scraper via a `.env` file (see `.env.example`).
- **Robust Refactoring**: Better error handling and more maintainable code structure.
- **Unit Tests**: Built-in tests to ensure reliability of data processing.

## 📚 Documentation
For detailed usage guides, code examples, and advanced configuration, please see [DOCS.md](./DOCS.md).

### 🙏 Support the Project
If you find this tool helpful, consider making a donation:
[**Donate via Coinbase**](https://commerce.coinbase.com/checkout/820e33e8-b652-408f-8f33-713af2ff7732)

---

## *Disclaimer*
This project is solely for fun and personal use. It is not associated, affiliated, or in conjunction with Weedmaps in any way. Nor do they know it probably exists. Please contact Weedmaps directly before using this information or code for any public/for profit usage. I made this to help people, not make money! Don't sue me Weedmaps!
