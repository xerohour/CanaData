import os
import sys
from playwright.sync_api import sync_playwright

# Add root to sys.path
sys.path.append(os.getcwd())
from generate_report import generate_html_report

def verify_frontend():
    # 1. Generate Report
    mock_data = {
        'data': {
            'listings': [
                {
                    'name': 'Test Shop',
                    'web_url': 'https://weedmaps.com/dispensaries/test-shop',
                    'rating': 4.5,
                    'reviews_count': 100,
                    'avatar_image': {'original_url': 'https://images.weedmaps.com/static/avatar/dispensary.png'},
                    'type': 'dispensary',
                    'open_now': True,
                    'address': '123 Test St',
                    'city': 'Denver',
                    'todays_hours_str': '9:00am - 9:00pm',
                    'phone_number': '555-0199',
                    'menu_items_count': 50,
                    'license_type': 'Medical'
                }
            ]
        },
        'meta': {
            'total_listings': 1
        }
    }
    generate_html_report(mock_data, "Test Region")

    report_path = os.path.abspath("listing_report.html")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{report_path}")

        # 2. Check Skip Link
        skip_link = page.locator(".skip-link")
        # Check if it becomes visible on focus
        skip_link.focus()
        # Wait a bit for transition
        page.wait_for_timeout(500)

        # 3. Check Rating Badge
        rating_badge = page.get_by_role("img", name="Rating: 4.5 stars based on 100 reviews")
        if rating_badge.count() > 0:
            print("✅ Rating badge with ARIA label found.")
        else:
            print("❌ Rating badge not found or ARIA label incorrect.")

        # 4. Check View Button
        view_btn = page.get_by_role("link", name="View Test Shop on Weedmaps (opens in a new tab)")
        if view_btn.count() > 0:
            print("✅ View button with ARIA label found.")
            # Check rel attribute
            rel = view_btn.get_attribute("rel")
            if rel == "noopener noreferrer":
                print("✅ View button has correct rel attribute.")
            else:
                print(f"❌ View button has incorrect rel attribute: {rel}")
        else:
            print("❌ View button not found or ARIA label incorrect.")

        # Screenshot of the card
        # We need to make sure the card is visible.
        page.locator(".card").first.screenshot(path="listing_card.png")
        print("✅ Screenshot saved to listing_card.png")

        browser.close()

if __name__ == "__main__":
    verify_frontend()
