from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # Launching a Browser
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://reddit.com")

    # Waiting for Elements
    page.wait_for_selector("main")  # Wait Until the <main> appears

    # Click an anchor with a text, "About Reddit"

    # Wheel to go 150 pxl, 1000 pxl
