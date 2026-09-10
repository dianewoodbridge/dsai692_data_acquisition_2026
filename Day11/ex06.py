from collections import defaultdict
import json

import asyncio

from playwright.async_api import async_playwright, Playwright
from playwright_stealth import Stealth


async def retrieve_content(playwright: Playwright, website_url: str) -> dict:
    """
    Goto nytimes.com/books/best-sellers/
    and retrieve Date, Genre, Book Name, Author, Bookshop.org URL as a dictionary,
    with Genre as keys.
    """
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch()
    page = await browser.new_page()
    await page.goto(website_url)

    genre_data = defaultdict(list)
    time = page.locator('time').first
    genre_data["Date"] = await time.text_content()
    # Find all genre elements (h2)
    genre_elements = await page.locator('h2').all()

    for genre_element in genre_elements:
        genre_name = await genre_element.text_content()

        # Find the following ordered list (ol) and then all list items (li) within it
        list_items = await genre_element.locator('xpath=following-sibling::ol[1]/li').all()

        for i, list_item in enumerate(list_items):
            book_name_element = list_item.locator('h3[itemprop="name"]').first
            book_author_element = list_item.locator(
                'p[itemprop="author"]').first
            bookshop_link_element = list_item.locator(
                'a:has-text("Bookshop.org")').first

            book_name = await book_name_element.text_content() if book_name_element else "Name Not Found"
            book_author = await book_author_element.text_content() if book_author_element else "Author Not Found"
            bookshop_url = await bookshop_link_element.get_attribute("href") if bookshop_link_element else "Bookshop.org URL Not Found"

            genre_data[genre_name.strip()].append({"name": book_name.strip(
            ), "author": book_author.replace("by ", "").strip(), "bookshop_url": bookshop_url})

    await browser.close()
    return genre_data


async def retrieve_bookshop_price(url, book_type="Ebook") -> float or None:
    """
    Retrieve the price of book_type from bookshop.org
    A valid url should include a bookshop.org.
    Possible book_type includes "Ebook", "Paperback", "Hardback"
    """
    if "bookshop.org" not in url:
        raise "Invalid URL"
    async with Stealth().use_async(async_playwright()) as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.screenshot(path=f"screenshot/{url}.png")

            # Find the element containing the text "book_type"
            book_element = page.locator(f'p:has-text("{book_type}")').first
            if await book_element.count() > 0:
                # The current bookshop.org structure, comes <div><div><p> Ebook</p></div></div><div><p>$price</p></div>
                container_elements = book_element.locator(
                    # Traverse up one level (example)
                    'xpath=../../following-sibling::div').first
                price = await container_elements.text_content()

            else:
                print(f"{book_type} format not found on the page.")

            await browser.close()
            return float(price.strip().split("$")[-1])
        except:
            await browser.close()
            return None


async def main():
    async with async_playwright() as playwright:
        h2_li_data = await retrieve_content(playwright,
                                            "https://www.nytimes.com/books/best-sellers/")

    for key, value in h2_li_data.items():
        if key != "Date":
            for item in value:
                url = item["bookshop_url"]
                bookshop_ebook_price = await retrieve_bookshop_price(url, "Ebook")
                item["bookshop_ebook_price"] = bookshop_ebook_price

    with open("output.json", "w") as f:
        json.dump(h2_li_data, f, indent=4)


data = asyncio.run(main())
