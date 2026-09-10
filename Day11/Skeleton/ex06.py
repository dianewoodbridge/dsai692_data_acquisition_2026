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


async def retrieve_bookshop_price(url, book_type="Ebook") -> float or None:
    """
    Retrieve the price of book_type from bookshop.org
    A valid url should include a bookshop.org.
    Possible book_type includes "Ebook", "Paperback", "Hardback"
    """


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
