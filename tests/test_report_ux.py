import os
import sys
from datetime import datetime

# Ensure we can import generate_report
sys.path.append(os.getcwd())

from generate_report import generate_html_report

def test_report_generation_ux():
    """
    Verifies that the generated HTML report contains specific UX and accessibility elements.
    """
    print("🧪 Starting UX Verification for Report Generation...")

    # Mock Data
    mock_data = {
        'meta': {'total_listings': 5},
        'data': {
            'listings': [
                {
                    'name': 'Test Dispensary',
                    'slug': 'test-dispensary',
                    'wmid': 12345,
                    'type': 'dispensary',
                    'rating': 4.5,
                    'reviews_count': 100,
                    'open_now': True,
                    'avatar_image': {'original_url': 'https://example.com/avatar.png'},
                    'address': '123 Main St',
                    'city': 'Test City',
                    'todays_hours_str': '9am - 9pm',
                    'phone_number': '555-0199',
                    'menu_items_count': 50,
                    'web_url': 'https://weedmaps.com/test',
                    'license_type': 'recreational',
                    'promo_code': {'code': 'SAVE10', 'title': 'Save 10%'}
                }
            ]
        }
    }

    report_path = 'test_ux_report.html'

    # Generate Report
    try:
        generate_html_report(mock_data, region_name="Test Region", filename=report_path)
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)

    if not os.path.exists(report_path):
        print("❌ Report file not created.")
        sys.exit(1)

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Checks
    checks = [
        ('Skip Link', '<a href="#main-content" class="skip-link">'),
        ('Main Content ID', 'id="main-content"'),
        ('Semantic Table Header', '<th scope="row" class="label">'),
        ('Lazy Loading', 'loading="lazy"'),
        ('ARIA Label', 'aria-label="View Test Dispensary on Weedmaps (opens in new tab)"'),
        ('Focus Styles', ':focus-visible'),
        ('Image Alt Text', 'alt="Test Dispensary logo"')
    ]

    all_passed = True
    for name, substring in checks:
        if substring in content:
            print(f"✅ {name} Check Passed")
        else:
            print(f"❌ {name} Check Failed! Expected to find substring")
            print(f"   Target: {substring}")
            all_passed = False

    # Clean up
    try:
        os.remove(report_path)
    except:
        pass

    if all_passed:
        print("\n🎉 All UX/A11y checks passed!")
    else:
        print("\n⚠️ Some checks failed.")
        sys.exit(1)

if __name__ == "__main__":
    test_report_generation_ux()
