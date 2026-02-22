import json
import os
from datetime import datetime
from CanaData import CanaData

"""
HTML Report Generator Module

This module is responsible for analyzing the scraped data and producing a high-quality,
consumer-facing HTML report. It uses a modern, "Glassmorphism" design aesthetic
to present cannabis listing data in a visually appealing way.
"""

def generate_html_report(data, region_name="Colorado"):
    """
    Generates a premium HTML report from Weedmaps listing data.
    
    This function takes the raw JSON response from the Weedmaps discovery API and
    transforms it into a standalone HTML file (`listing_report.html`).
    
    The report features:
    - **Glassmorphism Design**: Translucent cards, blurred backgrounds, and neon accents.
    - **Responsive Grid**: Automatically adjusts columns based on screen size.
    - **Rich Metadata**: Displays ratings, reviews, open status, and promo codes.
    - **Direct Links**: 'View on Weedmaps' buttons for quick navigation.
    
    Args:
        data (dict): The raw JSON dictionary returned by `CanaData.do_request`.
        region_name (str): The display name for the region header (default: "Colorado").
        
    Output:
        Creates a file named `listing_report.html` in the current working directory.
    """
    listings = data.get('data', {}).get('listings', [])
    meta = data.get('meta', {})
    total_listings = meta.get('total_listings', len(listings))
    
    # Modern CSS with Glasmorphism and Vibrant Colors
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

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

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

    header {
        text-align: center;
        margin-bottom: 4rem;
        padding: 3rem;
        background: var(--glass);
        backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .meta-summary {
        font-size: 1.2rem;
        color: var(--text-muted);
    }

    .container {
        max-width: 1400px;
        margin: 0 auto;
    }

    .listing-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
        gap: 2rem;
    }

    .card {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        flex-direction: column;
    }

    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0, 255, 163, 0.1);
        border-color: rgba(0, 255, 163, 0.3);
    }

    .card-header {
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        border-bottom: 1px solid var(--glass-border);
    }

    .avatar {
        width: 80px;
        height: 80px;
        border-radius: 16px;
        object-fit: cover;
        background: var(--glass);
        border: 2px solid var(--glass-border);
    }

    .listing-info h2 {
        font-size: 1.4rem;
        margin-bottom: 0.25rem;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-type { background: rgba(0, 212, 255, 0.2); color: var(--secondary); }
    .badge-rating { background: rgba(245, 158, 11, 0.2); color: var(--accent); }
    .badge-open { background: rgba(0, 255, 163, 0.2); color: var(--primary); }
    .badge-closed { background: rgba(239, 68, 68, 0.2); color: #ef4444; }

    .card-body {
        padding: 1.5rem;
        flex-grow: 1;
    }

    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }

    .data-table tr {
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }

    .data-table td {
        padding: 0.75rem 0;
    }

    .label {
        color: var(--text-muted);
        width: 140px;
    }

    .value {
        font-weight: 500;
        text-align: right;
    }

    .promo-section {
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(245, 158, 11, 0.05);
        border: 1px dashed var(--accent);
        border-radius: 12px;
    }

    .promo-title {
        color: var(--accent);
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }

    .promo-body {
        font-size: 0.85rem;
    }

    .footer-actions {
        padding: 1.5rem;
        background: rgba(0, 0, 0, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .btn {
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }

    .btn-primary {
        background: var(--primary);
        color: var(--bg);
    }

    .btn-primary:hover {
        background: #00e692;
        box-shadow: 0 0 15px rgba(0, 255, 163, 0.4);
    }

    .btn:focus-visible {
        outline: 2px solid var(--text);
        outline-offset: 2px;
        box-shadow: 0 0 0 4px rgba(0, 255, 163, 0.4);
    }

    .skip-link {
        position: absolute;
        top: -40px;
        left: 0;
        background: var(--primary);
        color: var(--bg);
        padding: 8px;
        z-index: 100;
        transition: top 0.2s;
        font-weight: bold;
        text-decoration: none;
        border-radius: 0 0 8px 0;
    }

    .skip-link:focus {
        top: 0;
    }

    @media (max-width: 768px) {
        body { padding: 1rem; }
        header { padding: 2rem 1rem; margin-bottom: 2rem; }
        h1 { font-size: 2rem; }
        .listing-grid { grid-template-columns: 1fr; }
    }
    """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weedmaps Discovery Report - {region_name}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
        <style>{css}</style>
    </head>
    <body>
        <a href="#main-content" class="skip-link">Skip to main content</a>
        <div class="container">
            <header>
                <h1>{region_name} Discovery</h1>
                <p class="meta-summary">Found {total_listings} matches in the region • Generated on {datetime.now().strftime('%b %d, %Y')}</p>
            </header>

            <main id="main-content" class="listing-grid">
    """

    for item in listings:
        avatar = item.get('avatar_image', {}).get('original_url', 'https://images.weedmaps.com/static/avatar/dispensary.png')
        rating = item.get('rating', 'N/A')
        reviews = item.get('reviews_count', 0)
        is_open = item.get('open_now', False)
        status_text = "Open Now" if is_open else "Closed"
        status_class = "badge-open" if is_open else "badge-closed"
        
        promo = item.get('promo_code')
        promo_html = ""
        if promo:
            promo_html = f"""
            <div class="promo-section">
                <div class="promo-title">✨ PROMO: {promo.get('code', 'Special Offer')}</div>
                <div class="promo-body">{promo.get('title', 'Check website for details')}</div>
            </div>
            """

        html_content += f"""
                <div class="card">
                    <div class="card-header">
                        <img src="{avatar}" alt="{item.get('name')}" class="avatar">
                        <div class="listing-info">
                            <h2>{item.get('name')}</h2>
                            <span class="badge badge-type">{item.get('type')}</span>
                            <span class="badge badge-rating">★ {rating} ({reviews})</span>
                            <span class="badge {status_class}">{status_text}</span>
                        </div>
                    </div>
                    <div class="card-body">
                        <table class="data-table">
                            <tr>
                                <td class="label">Address</td>
                                <td class="value">{item.get('address', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td class="label">City</td>
                                <td class="value">{item.get('city', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td class="label">Hours Today</td>
                                <td class="value">{item.get('todays_hours_str', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td class="label">Phone</td>
                                <td class="value">{item.get('phone_number', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td class="label">Menu Items</td>
                                <td class="value">{item.get('menu_items_count', 0)} items</td>
                            </tr>
                        </table>
                        {promo_html}
                    </div>
                    <div class="footer-actions">
                        <span style="font-size: 0.8rem; color: var(--text-muted)">{item.get('license_type', 'Recreational')}</span>
                        <a href="{item.get('web_url')}" target="_blank" class="btn btn-primary" aria-label="View {item.get('name')} on Weedmaps">View on Weedmaps</a>
                    </div>
                </div>
        """

    html_content += """
            </main>
        </div>
    </body>
    </html>
    """
    
    with open('listing_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Success! Report generated: {os.path.abspath('listing_report.html')}")

if __name__ == "__main__":
    print("🚀 Fetching live data for Colorado...")
    cana = CanaData()
    # Use the Colorado discovery URL with a larger page size for a better report
    url = "https://api-g.weedmaps.com/discovery/v1/listings?filter[any_retailer_services][]=storefront&filter[any_retailer_services][]=delivery&filter[region_slug[deliveries]]=colorado&filter[region_slug[dispensaries]]=colorado&page_size=24&size=24"
    
    data = cana.do_request(url)
    if data and data != 'break':
        generate_html_report(data)
    else:
        print("❌ Failed to retrieve data from Weedmaps.")
