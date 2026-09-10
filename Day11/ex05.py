import asyncio
from playwright.async_api import async_playwright


async def scrape_page(url, p):
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto(url)
    title = await page.title()
    await browser.close()
    return title


async def main():
    async with async_playwright() as p:
        # Below is the same as the following commented block
        # results = await asyncio.gather(scrape_page("https://reddit.com", p),
        #                                scrape_page("https://linkedin.com", p))
        urls = ["https://reddit.com", "https://linkedin.com"]
        results = await asyncio.gather(*(scrape_page(url, p) for url in urls))
        print(results)

asyncio.run(main())
