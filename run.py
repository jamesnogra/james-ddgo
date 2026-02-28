from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
import json

NAME_STRING_TO_SEARCH = 'james arnold nogra'

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
        
        # Keep the window open for 10 seconds to view results
        time.sleep(5)

        # Click "More results" at the bottom
        for i in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            try:
                more_results_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'More results')]"))
                )
                # 3. Click it
                more_results_button.click()
                print("Clicked 'More results' successfully!")
                time.sleep(5)
            except Exception as e:
                print('Reached the end of results')
                break

        # Get all link results
        all_results = driver.find_elements(By.XPATH, "//a[@data-testid='result-title-a']")
        link_results = []
        # Loop through and print each one
        for index, result in enumerate(all_results, 1):
            url = result.get_attribute("href")
            title = result.text
            #print(f"{index}. {title} -> {url}")
            link_results.append({
                'title': title,
                'url': url
            })
        print(json.dumps(link_results, indent=4, sort_keys=True))

        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = f"https://duckduckgo.com/?ia=web&origin=funnel_home_website&t=h_&q={NAME_STRING_TO_SEARCH}&chip-select=search"
    open_stealth_browser(target_url)