from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import json
import csv

NAME_STRING_TO_SEARCH = 'james arnold nogra'

link_results = []

def open_stealth_browser(url):
    # 1. Setup Chrome Options
    options = Options()
    # Optional: Run headless if you don't want a window to pop up
    # options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    # 3. Apply Selenium-Stealth to mask fingerprints
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="MacIntel", # Standard platform string for macOS
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        time.sleep(5)

        # Scroll at the bottom of the page to load more images
        for i in range(1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

        # Get all the image elements li
        list_items = driver.find_elements(By.XPATH, "//figure[descendant::img]")
        for item in list_items:
            try:
                # Find the <img> tag inside this specific figure
                # .//img means "search for any img descendant of THIS element"
                img_element = item.find_element(By.XPATH, ".//img")
                img_src = img_element.get_attribute("src")
                # Find the <a> tag inside this specific figure
                a_element = item.find_element(By.XPATH, ".//a")
                link_href = a_element.get_attribute("href")
                # Optional: Grab the title text while you're at it
                title_text = a_element.text
                link_results.append({
                    "image": img_src,
                    "link": link_href,
                    "title": title_text
                })
            except Exception as e:
                print(f"Skipping an item due to error: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def write_results_to_file():
    filename = f"results-images-{NAME_STRING_TO_SEARCH}.csv"
    headers = link_results[0].keys()
    # 3. Write to the file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # Write the header row (title, url)
        writer.writeheader()
        # Write all the data rows
        writer.writerows(link_results)

target_url = f'https://duckduckgo.com/?q=%22"{NAME_STRING_TO_SEARCH}"%22&t=h_&ia=images&iax=images'
open_stealth_browser(target_url)
write_results_to_file()