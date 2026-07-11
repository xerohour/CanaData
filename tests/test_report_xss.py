def test_xss_in_html_report_javascript_uri():
    """Test that javascript: URIs in avatar and web_url are neutralized and CSP is present."""
    from generate_report import generate_html_report
    import os

    malicious_data = {
        'data': {
            'listings': [
                {
                    'name': 'Test Dispensary',
                    'avatar_image': {'original_url': 'javascript:alert(1)'},
                    'web_url': 'javascript:alert(2)'
                }
            ]
        },
        'meta': {'total_listings': 1}
    }

    generate_html_report(malicious_data, region_name="Test")

    with open('listing_report.html', 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'javascript:alert' not in content, "Malicious javascript URI found in HTML output"
    assert '<meta http-equiv="Content-Security-Policy"' in content, "CSP tag missing"

    if os.path.exists('listing_report.html'):
        os.remove('listing_report.html')
