from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launching a Browser
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://reddit.com")

    # Waiting for Elements
    page.wait_for_selector("main")  # Wait Until the <main> appears

    # Select Elements
    for anchor in page.query_selector_all("a"):  # Return <a>
        print(anchor.inner_text().strip())
        print(anchor.get_attribute("href"))  # Return href's values in <a>
    browser.close()
