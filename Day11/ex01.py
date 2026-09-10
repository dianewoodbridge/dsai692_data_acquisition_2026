from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Step 1. Create a browser
    # Can use chromium/firefox/webkit
    browser = p.chromium.launch(headless=False)

    # Step 2. Create a new BrowserContext
    context = browser.new_context()
    page = context.new_page()

    # Step 3. Open a page
    page.goto("https://medium.com/tag/artificial-intelligence")

    print(page.title())  # Returns the page's title.
    page.wait_for_selector("main")  # Wait Until the <main> appears

    article = page.query_selector("article")  # Return a single <article>
    print(article.inner_text())

    for elem in page.query_selector_all("article"):  # Return all <article>
        print(elem.inner_text())
