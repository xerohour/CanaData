from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("file:///app/listing_report.html")
    page.screenshot(path="listing_report_screenshot.png", full_page=True)
    browser.close()
