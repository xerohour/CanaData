import os
import pytest
from generate_report import generate_html_report

def test_generate_html_report_accessibility():
    """
    Test that the generated HTML report includes key accessibility features.
    """
    # Mock data
    mock_data = {
        "meta": {"total_listings": 1},
        "data": {
            "listings": [
                {
                    "name": "Test Dispensary",
                    "type": "dispensary",
                    "rating": 4.5,
                    "reviews_count": 100,
                    "open_now": True,
                    "address": "123 Green St",
                    "city": "Denver",
                    "todays_hours_str": "9am - 9pm",
                    "phone_number": "555-0199",
                    "menu_items_count": 50,
                    "web_url": "https://weedmaps.com/dispensaries/test",
                    "avatar_image": {"original_url": "http://example.com/img.png"}
                }
            ]
        }
    }

    output_file = "test_report.html"

    try:
        # Generate the report
        generate_html_report(mock_data, region_name="Test Region", output_file=output_file)

        # Read the generated file
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for Skip Link
        assert '<a href="#main-content" class="skip-link">Skip to content</a>' in content

        # Check for Main Landmark
        assert '<main id="main-content" class="listing-grid">' in content

        # Check for Focus Styles
        assert '.skip-link:focus' in content
        assert ':focus-visible' in content

        # Check for ARIA Label
        assert 'aria-label="View Test Dispensary on Weedmaps"' in content

    finally:
        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)
