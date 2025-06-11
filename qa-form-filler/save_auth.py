# save_auth.py

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Launch with GUI
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://yourwebsite.com")  # Replace with your actual login URL

    print("Please log in manually in the opened browser window.")
    input("Press Enter here *after* you've successfully logged in...")

    context.storage_state(path="auth.json")
    print("Auth state saved to 'auth.json'.")

    browser.close()