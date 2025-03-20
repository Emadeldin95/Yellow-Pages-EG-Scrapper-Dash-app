import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import threading
import pandas as pd


class YellowPagesScraper:
    def __init__(self):
        self.data = []
        self.scraping = False
        self.scraped_count = 0
        self.driver = None
        self.base_url = "https://yellowpages.com.eg/en/search/"

    def start_driver(self):
        """Start an undetected Chrome browser session."""
        options = uc.ChromeOptions()
        options.headless = False
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = uc.Chrome(options=options)

    def start_scraping(self, keyword, max_companies=None):
        """Start scraping process."""
        if self.scraping:
            return

        self.scraping = True
        self.scraped_count = 0
        self.data = []
        thread = threading.Thread(target=self._scrape, args=(keyword, max_companies))
        thread.start()

    def _scrape(self, keyword, max_companies):
        """Scrape YellowPages using Selenium."""
        self.start_driver()

        search_url = f"{self.base_url}{keyword}"
        self.driver.get(search_url)
        time.sleep(5)  # ✅ Restored previous wait time for page load

        page_number = 1
        total_companies_scraped = 0

        while self.scraping:
            print(f"Scraping page {page_number}...")

            # ✅ Restored previous scrolling behavior
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3)
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
            time.sleep(3)

            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "item-title")))
            except Exception:
                print("Bot detected or no data available.")
                break

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            company_blocks = self.driver.find_elements(By.CLASS_NAME, "col-xs-12.item-details")

            for block in company_blocks:
                if not self.scraping:
                    break

                name = block.find_element(By.CLASS_NAME, "item-title").text.strip() if block.find_elements(
                    By.CLASS_NAME, "item-title") else 'N/A'
                address = block.find_element(By.CLASS_NAME, "address-text").text.strip() if block.find_elements(
                    By.CLASS_NAME, "address-text") else 'N/A'

                # ✅ Restored proper phone number extraction logic
                phone = "N/A"
                try:
                    phone_button = block.find_element(By.CLASS_NAME, "call-us-click")
                    self.driver.execute_script("arguments[0].click();", phone_button)
                    time.sleep(2)  # ✅ Restored delay to allow phone pop-up to load

                    popover = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "popover-content")))
                    phone_numbers = [a.text.strip() for a in popover.find_elements(By.TAG_NAME, "a")]
                    phone = ", ".join(phone_numbers) if phone_numbers else "N/A"
                except Exception as e:
                    print(f"Warning: Could not extract phone number for {name}: {e}")

                website = block.find_element(By.CLASS_NAME, "website").get_attribute("href") if block.find_elements(
                    By.CLASS_NAME, "website") else 'N/A'

                self.data.append({
                    "name": name,
                    "phone": phone,
                    "address": address,
                    "website": website
                })

                self.scraped_count += 1

                total_companies_scraped += 1
                if max_companies and total_companies_scraped >= max_companies:
                    self.scraping = False
                    break

            try:
                next_page = self.driver.find_element(By.XPATH, "//a[@aria-label='Next']")
                self.driver.execute_script("arguments[0].click();", next_page)
                time.sleep(5)  # ✅ Restored transition delay
                page_number += 1
            except Exception:
                break

        self.driver.quit()
        self.scraping = False
        print(f"Scraping complete. {len(self.data)} companies found.")

    def stop_scraping(self):
        """Stop the scraping process."""
        self.scraping = False

    def get_data(self):
        """Return the latest scraped data."""
        return self.data

    def get_status(self):
        """Return scraping status and count."""
        status = "Scraping" if self.scraping else "Idle"
        return {"status": status, "scraped_count": self.scraped_count}
