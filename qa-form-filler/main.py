from cli import get_args
from logging_config import setup_logger
import logging
import json
from pathlib import Path
from faker import Faker
from urllib.parse import urlparse
from datetime import datetime
import os
import random
import csv
import time

def log_field_fill(domain, label, value, success=True):
    date_str = datetime.now().strftime('%Y%m%d')
    log_dir = Path("logs") / domain / date_str
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "form_data_log.csv"
    with open(log_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([label, value, "success" if success else "failed"])

def process_with_playwright(args, urls):
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
    fake = Faker()
    os.makedirs("screenshots", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = browser.new_context()

        for i, entry in enumerate(urls):
            page = context.new_page()
            try:
                url = entry["url"]
                domain = urlparse(url).netloc.replace('.', '_')
                logging.info(f"Opening {url}")
                page.goto(url, timeout=60000)
                page.wait_for_timeout(2000)

                all_elements = page.query_selector_all('input, textarea, select')
                for field in all_elements:
                    try:
                        if not field.is_enabled():
                            continue

                        tag = field.evaluate("el => el.tagName.toLowerCase()")
                        input_type = field.get_attribute("type") or ""
                        name = field.get_attribute("name") or field.get_attribute("id") or ""
                        label = name.lower() if name else f"{tag}_{input_type}"

                        if tag == "input":
                            if input_type == "date":
                                value = datetime.today().strftime("%Y-%m-%d")
                                field.evaluate("(el, val) => el.value = val", value)
                            elif input_type == "email":
                                value = fake.email()
                                field.fill(value)
                            elif input_type == "text":
                                if "first" in label:
                                    value = fake.first_name()
                                elif "last" in label:
                                    value = fake.last_name()
                                elif "name" in label:
                                    value = fake.name()
                                elif "zip" in label or "postal" in label:
                                    value = fake.postcode()
                                elif "city" in label:
                                    value = fake.city()
                                else:
                                    value = fake.word()
                                field.fill(value)
                            elif input_type == "tel":
                                value = fake.phone_number()
                                field.fill(value)
                            elif input_type == "number":
                                value = str(random.randint(1, 100))
                                field.fill(value)
                            elif input_type == "checkbox":
                                if random.choice([True, False]):
                                    field.check()
                                    value = "checked"
                                else:
                                    field.uncheck()
                                    value = "unchecked"
                            elif input_type == "radio":
                                if not field.is_checked():
                                    field.check()
                                value = "selected"
                            elif input_type == "color":
                                value = "#%06x" % random.randint(0, 0xFFFFFF)
                                field.evaluate("(el, val) => el.value = val", value)
                            else:
                                value = "skipped"
                        elif tag == "textarea":
                            value = fake.text()
                            field.fill(value)
                        elif tag == "select":
                            options = field.query_selector_all("option")
                            if options:
                                selected = options[random.randint(0, len(options)-1)]
                                value = selected.get_attribute("value") or selected.inner_text()
                                field.select_option(value)
                        else:
                            value = "tested"

                        log_field_fill(domain, label, value, success=True)
                        logging.info(f"Filled field '{label}' with '{value}'")

                    except Exception as inner_e:
                        log_field_fill(domain, label, "", success=False)
                        logging.warning(f"Could not fill field '{label}': {inner_e}")

                if args.submit:
                    button = page.query_selector("form button[type='submit'], button[type='submit']")
                    if button:
                        button.click()
                page.wait_for_timeout(2000)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"form_{i}_{domain}_{timestamp}.png"
                screenshot_path = os.path.join("screenshots", filename)
                page.screenshot(path=screenshot_path, full_page=True)
                logging.info(f"Screenshot saved to {screenshot_path}")

            except PlaywrightTimeoutError:
                logging.error(f"Timeout while processing {url}")
            except Exception as e:
                logging.error(f"Error processing {url}: {e}")
            finally:
                page.close()

        browser.close()

def process_with_selenium(args, urls):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    fake = Faker()
    os.makedirs("screenshots", exist_ok=True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    for i, entry in enumerate(urls):
        try:
            url = entry["url"]
            domain = urlparse(url).netloc.replace('.', '_')
            logging.info(f"Opening {url}")
            driver.get(url)

            time.sleep(2)
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for field in inputs:
                try:
                    input_type = field.get_attribute("type") or ""
                    name = field.get_attribute("name") or field.get_attribute("id") or ""
                    label = name.lower() if name else input_type

                    value = ""
                    if input_type == "date":
                        value = datetime.today().strftime("%Y-%m-%d")
                    elif input_type == "email":
                        value = fake.email()
                    elif "name" in label:
                        value = fake.name()
                    elif "zip" in label:
                        value = fake.postcode()
                    else:
                        value = fake.word()

                    field.clear()
                    field.send_keys(value)
                    log_field_fill(domain, label, value, success=True)
                except Exception as e:
                    log_field_fill(domain, label, "", success=False)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/form_{i}_{domain}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            logging.error(f"Error processing {url}: {e}")

    driver.quit()

def main():
    args = get_args()
    setup_logger()
    logging.info("Logger initialized.")

    with open(args.urls, "r") as f:
        urls = json.load(f)

    if args.login:
        from save_auth import login_and_save_auth
        login_and_save_auth(auth_file=args.auth or "auth.json")

    if args.selenium:
        process_with_selenium(args, urls)
    else:
        process_with_playwright(args, urls)

if __name__ == "__main__":
    main()
