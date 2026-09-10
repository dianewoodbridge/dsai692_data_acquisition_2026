from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launching a Browser
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://reddit.com")

    # Waiting for Elements
    # Wait Until the <main> appears

    # Select Elements
