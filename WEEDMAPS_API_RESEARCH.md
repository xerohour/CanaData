# Weedmaps API Endpoints Research

## Current Implementation Analysis

Based on the existing `CanaData.py` implementation, the project currently uses:

### Discovery API (Public/Undocumented)
- **Base URL**: `https://api-g.weedmaps.com/discovery/v1/listings`
- **Purpose**: Retrieve dispensary and delivery listings by region
- **Current Usage**:
  ```python
  # Line 16 in CanaData.py
  self.baseUrl = 'https://api-g.weedmaps.com/discovery/v1/listings'
  ```

### Web API (Public/Undocumented)
- **Base URL**: `https://weedmaps.com/api/web/v1/listings/{slug}/menu`
- **Purpose**: Retrieve menu data for specific listings
- **Current Usage**:
  ```python
  # Line 162 in CanaData.py
  url = f'https://weedmaps.com/api/web/v1/listings/{location["slug"]}/menu?type={location["type"]}'
  ```

---

## Official Weedmaps Partner APIs

Weedmaps provides documented APIs for integration partners. These require OAuth 2.0 authentication and partner credentials.

### 1. Menu API
**Base URL**: `https://api-g.weedmaps.com/wm/`

**Key Endpoints**:
- **Brands**: `GET /wm/{version}/partners/brands`
  - Retrieve brand information with filtering and sorting
  - Versions: `2023.07`, `2024.01`, `2024.07`, `2025.01`, `2025.07`, `2026.01`
  - Example: `https://api-g.weedmaps.com/wm/2026-01/partners/brands`

- **Brand Products**: `GET /wm/{version}/partners/brands/{brand_id}/products`
  - Find products associated with specific brands
  - Example: `/wm/2024-01/partners/brands/{brand_id}/products`

- **Menu Items**: `GET /partners/menus/{menu_id}/items`
  - Retrieve items from a specific menu
  - Supports product classification and structured data (cannabinoids, terpenes, strains)

**Features**:
- Real-time menu synchronization
- Product enrichment with taxonomy data
- Category, cannabinoid, terpene, and strain information
- Enhanced search relevance and consumer engagement

**Authentication**: OAuth 2.0 access token required

**Pagination**: Uses `_page` and `_limit` parameters

### 2. Orders API
**Base URL**: `https://api-g.weedmaps.com/oos/`

**Key Endpoints**:
- **Update Order**: `PUT /oos/{version}/merchants/{listing_id}/orders/{order_id}`
  - Versions: `2024.01`, `2026.01`
  - Example: `/oos/2026-01/merchants/{merchantId}/orders/{orderId}`

**Features**:
- Receive and manage online orders in POS systems
- Two-way order status updates
- Integrated delivery flow support
- Eliminates manual order entry

**Authentication**: OAuth 2.0 access token required

---

## Alternative Undocumented Endpoints

Based on reverse-engineering and community findings:

### Validated Public Endpoints (No Auth Required)
Recent testing confirmed the following endpoints are accessible without authentication via `curl` (note: `requests` library may require specific headers to avoid 406 errors):

1. **Listings**: `https://api-g.weedmaps.com/discovery/v1/listings`
   - Primary endpoint for finding dispensaries and deliveries.
   - Requires `filter[region_slug[dispensaries]]` or similar filters.

2. **Brands**: `https://api-g.weedmaps.com/discovery/v1/brands`
   - Returns a list of cannabis brands with IDs, ratings, and avatars.
   - Useful for building a brand database.

3. **Products**: `https://api-g.weedmaps.com/discovery/v1/products`
   - Returns a global list of products.
   - Includes price statistics and associated listing info.

4. **Categories**: `https://api-g.weedmaps.com/discovery/v1/categories`
   - Returns the taxonomy of cannabis products (Flower, Edibles, Vapes, etc.).
   - Useful for mapping and filtering menus.

5. **Deals**: `https://api-g.weedmaps.com/discovery/v1/deals`
   - Returns active deals and promotions.
   - Includes metadata about discount types and which listings offer them.

6. **Discovery Tags**: `https://api-g.weedmaps.com/discovery/v1/discovery_tags`
   - Returns smart labels (e.g., "Sleepy," "Focused") that power the "By Effect" filters.
   - Essential for mapping product intent to consumer search behavior.

7. **Search**: `https://api-g.weedmaps.com/discovery/v1/search?q={query}`
   - Global search across listings, products, and brands.
   - Highly useful for cross-referencing by name.

7. **Strains** (Potential): `https://api-g.weedmaps.com/discovery/v1/strains`
   - Researching availability for global strain database.

---

## Cross-Reference Identifiers

To link Weedmaps data with other platforms (Leafly, CannMenus, regulators), the following fields are the most reliable:

### 1. Global Identifiers
- **WMID (Weedmaps ID)**: Found in listing data (`wmid: 307584908`). Used across most Weedmaps endpoints.
- **UUID**: Used for Categories (`uuid: "a780af3d-bdfe-41ce-a782-20f2519fd7be"`) and potentially products. These are more stable than primary keys.
- **License Numbers**: Found in listing details. This is the "Gold Standard" for cross-referencing against State databases (METRC, BioTrack).

### 2. Product-Level Identifiers
- **menu_item_id**: Unique to a specific product instance at a specific location.
- **variant_slug**: A unique string representing a product variety (e.g., `wyld-gummies-raspberry-sativa-962bc461...`).
- **Brand ID/Slug**: Used to link products to their manufacturers.

## Addressing the 406 "Not Acceptable" Error

During research, Python's `requests` library consistently received 406 errors while `curl` succeeded. This suggests Weedmaps' security (likely Kong/Varnish) is fingerprints Python-requests.

### Recommended Fixes for `CanaData.py`
To avoid these errors and future-proof the script, the following changes should be applied to the `do_request` method:

1. **Add Minimal Browser Headers**:
   ```python
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
       'Accept': 'application/json, text/plain, */*',
       'Accept-Language': 'en-US,en;q=0.9',
       'Origin': 'https://weedmaps.com',
       'Referer': 'https://weedmaps.com/'
   }
   req = requests.get(url, headers=headers)
   ```

2. **Handle 422 "Invalid Params"**:
   Weedmaps returns 422 when filters are missing (e.g., "region is required"). The script should log the `detail` field from the error response to help users debug their search slugs.

---

## Alternative Data Sources

---

## Alternative Data Sources

### 1. Leafly API
- **Platform**: Leafly.com
- **Access**: Apify Leafly Dispensary Scraper
- **Data Available**:
  - Dispensary addresses and contact details
  - Ratings and reviews
  - Operating hours
  - Delivery/pickup options
- **API**: Programmatic access via Apify API

### 2. CannMenus Cannabis Data API
- **Website**: [cannmenus.com](https://cannmenus.com)
- **API Base URL**: `https://api.cannmenus.com/v1`
- **Authentication**: `X-Token` header required.
- **Key Endpoints**:
  - `/retailers?state={STATE_CODE}`: Fetch retailers in a state.
  - `/retailers/{retailer_id}/menu`: Fetch full normalized menu.
  - `/products`: Search products globally with SKU grouping.
- **Features**:
  - Normalized, production-ready cannabis market data.
  - Multi-platform aggregation (standardizes data from various POS/menu systems).
  - Significant U.S. dispensary coverage.

### 3. Advanced Anti-Bot Measures (Weedmaps)
Recent research indicates Weedmaps uses:
- **Fingerprinting**: Canvas, WebGL, and Audio context fingerprints to detect headless browsers.
- **Traffic Patterns**: Frequency and human-like movement analysis.
- **WAF/Security**: Likely Cloudflare or similar, which blocks the default `python-requests` User-Agent string (leading to 406 errors).
- **JavaScript Obfuscation**: Used to generate dynamic validation tokens for certain high-value endpoints.

### 3. Green Check Access API
- **Website**: greencheckverified.com
- **Focus**: Compliance and transactional data
- **Data Sources**: Leading POS and seed-to-sale systems
- **Use Cases**:
  - Consolidated reporting
  - Financial insights
  - Sales analytics
  - Operational data

### 4. Third-Party Scraping Services
- **Apify Weedmaps Scraper**: Extracts product names, categories, brands, prices
- **iWeb Scraping**: Professional Weedmaps/Leafly data extraction
- **DataScrapingServices.com**: Custom scraping solutions
- **WebsiteScraper.com**: Structured data delivery (CSV, Excel, JSON)

### 5. Other Cannabis APIs
Available on RapidAPI:
- Otreeba Open Cannabis API
- Strain API
- Neobi Open Cannabis API
- MAPI US

### 6. State Government Data Portals
- **Example**: PA Medical Marijuana Dispensaries (Data.gov)
- **Features**: Official facility details with API access
- **Availability**: Varies by state

---

## Reverse-Engineering Techniques

### Browser Developer Tools Method
1. Open Chrome/Firefox Developer Tools (F12)
2. Navigate to Network tab
3. Browse Weedmaps website
4. Filter by XHR/Fetch requests
5. Examine API calls made by the website
6. Copy request URLs and headers
7. Test endpoints with tools like Postman or curl

### JavaScript Analysis
1. View page source
2. Search for API endpoint patterns in JavaScript files
3. Look for base URLs and endpoint constructors
4. Identify authentication mechanisms
5. Extract query parameters and filters

### Mobile App Analysis
- Decompile mobile apps (Android APK)
- Examine network traffic with proxy tools (Charles, Burp Suite)
- Identify mobile-specific API endpoints
- Often less rate-limited than web APIs

---

## Implementation Recommendations

### Short-Term (No Authentication Required)
1. **Explore Discovery API filters**:
   - Test additional filter parameters
   - Implement location-based search
   - Add rating and availability filters

2. **Expand Web API usage**:
   - Test `/details`, `/reviews`, `/photos` endpoints
   - Retrieve deals and promotions
   - Collect operating hours data

3. **Add error handling**:
   - Implement exponential backoff for rate limiting
   - Add retry logic with delays
   - Log failed requests for analysis

### Medium-Term (Alternative Sources)
1. **Integrate Leafly scraper**:
   - Cross-reference Weedmaps data
   - Fill gaps in coverage
   - Validate pricing information

2. **Evaluate CannMenus API**:
   - Compare data quality
   - Assess coverage vs. Weedmaps
   - Test API performance and reliability

3. **Implement data aggregation**:
   - Combine multiple sources
   - Deduplicate listings
   - Normalize data formats

### Long-Term (Official Partnership)
1. **Apply for Weedmaps Partner API access**:
   - Contact Weedmaps integration team
   - Obtain OAuth credentials
   - Access official Menu and Orders APIs

2. **Build compliant integration**:
   - Follow official API documentation
   - Implement proper authentication
   - Respect rate limits and terms of service

---

## Rate Limiting Considerations

### Current Implementation Issues
- No explicit rate limiting in `CanaData.py`
- Relies on user intervention when errors occur (line 134-143)
- Could trigger anti-scraping measures

### Recommended Improvements
```python
import time
from random import uniform

# Add delay between requests
def do_request_with_backoff(self, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            # Random delay between 1-3 seconds
            time.sleep(uniform(1.0, 3.0))
            
            req = requests.get(url, timeout=30)
            
            if req.status_code == 200:
                return req.json()
            elif req.status_code == 429:  # Rate limited
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Error {req.status_code}: {req.text}")
                return False
                
        except Exception as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return False
    
    return False
```

---

## Legal and Ethical Considerations

### Terms of Service
- Review Weedmaps Terms of Service before scraping
- Undocumented APIs may violate ToS
- Official Partner APIs require agreement acceptance

### Data Usage
- Personal use vs. commercial use restrictions
- Attribution requirements
- Data redistribution limitations

### Best Practices
1. Respect robots.txt
2. Implement reasonable rate limiting
3. Use official APIs when available
4. Cache data to minimize requests
5. Provide user-agent identification
6. Don't overwhelm servers

### Disclaimer (from README.md)
> "This project is solely for fun and personal use. It is not associated, affiliated, or in conjunction with Weedmaps in any way. Please contact Weedmaps directly before using this information or code for any public/for profit usage."

---

## Testing Endpoints

### Example curl Commands

**Test Discovery API**:
```bash
curl -g "https://api-g.weedmaps.com/discovery/v1/listings?filter[any_retailer_services][]=storefront&filter[region_slug[dispensaries]]=california&page_size=10&size=10"
```

**Test Menu API**:
```bash
curl "https://weedmaps.com/api/web/v1/listings/example-dispensary/menu?type=dispensary"
```

**Test with Headers**:
```bash
curl -H "User-Agent: Mozilla/5.0" \
     -H "Accept: application/json" \
     "https://api-g.weedmaps.com/discovery/v1/listings?filter[region_slug[dispensaries]]=colorado&page_size=5"
```

---

## Next Steps

1. **Document Current Endpoints**:
   - Create endpoint inventory
   - Test response formats
   - Document required parameters

2. **Experiment with Variations**:
   - Test alternative filter combinations
   - Explore undocumented endpoints
   - Monitor for API changes

3. **Implement Monitoring**:
   - Track API availability
   - Log response times
   - Detect breaking changes

4. **Consider Alternatives**:
   - Evaluate Leafly integration
   - Test CannMenus API
   - Compare data quality

5. **Plan for Scale**:
   - Implement caching layer
   - Add database storage
   - Build data pipeline

---

## Resources

### Official Documentation
- [Weedmaps Integration Partners](https://weedmaps.com/integration-partners)
- [Weedmaps API Documentation](https://weedmaps.com/integration-partners/api-documentation)

### Alternative APIs
- [Apify Leafly Scraper](https://apify.com/apify/leafly-scraper)
- [CannMenus API](https://cannmenus.com/api)
- [Green Check API](https://greencheckverified.com/access-api)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [Insomnia](https://insomnia.rest/) - REST client
- [Charles Proxy](https://www.charlesproxy.com/) - Network debugging
- [Burp Suite](https://portswigger.net/burp) - Security testing

### Community
- [CanaData Discord](https://discord.gg/6WAcVek)
- GitHub Issues and Discussions

---

## Changelog

## Conclusion

The Weedmaps Discovery API is a rich, undocumented source of cannabis market data. While some endpoints like `/strains` are restricted or moved (returning 404), the `/products`, `/brands`, and `/search` endpoints provide sufficient metadata to build a comprehensive cross-referenced database.

**Key Action Items for Integration**:
1. **Use `license` fields** from listing data to cross-reference with METRC/State data.
2. **Leverage `menu_item_id` and `variant_slug`** for internal Weedmaps product tracking.
3. **Use the Global Search endpoint** (`/search?q=`) for fuzzy matching against other platforms like Leafly.
