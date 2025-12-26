from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_real_estate():
    print("🚀 Initializing Professional Browser Bot...")
    
    options = Options()
    # Masking the automation to avoid bot detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # We will try a slightly different page that is often more "scraper-friendly"
    url = "https://www.99acres.com/property-in-nagpur-ffid"
    driver.get(url)

    # 1. Wait for the page to settle
    time.sleep(5)

    # 2. SCROLL DOWN (Essential for Lazy Loading)
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(2)

    properties_data = []

    try:
        # 3. UNIVERSAL SELECTOR: Look for all "Property Cards"
        # We look for the most common container tags
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Get all text blocks and look for property patterns
        all_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='tuple'], div[class*='card'], article")
        
        print(f"🧐 Scanning {len(all_elements)} elements for property info...")

        for el in all_elements:
            text = el.text.strip()
            if text and "₹" in text: # Only grab items that have a price symbol
                lines = text.split('\n')
                properties_data.append({
                    "Raw Info": text[:100].replace('\n', ' | '), # First 100 chars
                    "Title": lines[0]
                })

        # Remove duplicates
        df = pd.DataFrame(properties_data).drop_duplicates()

    except Exception as e:
        print(f"❌ Error: {e}")
    
    if not properties_data:
        print("😭 Still found 0. Taking a screenshot for diagnosis...")
        driver.save_screenshot("diagnosis.png")
    else:
        df.to_csv("nagpur_listings.csv", index=False)
        print(f"✅ Success! Saved {len(df)} properties to nagpur_listings.csv")

    driver.quit()

if __name__ == "__main__":
    scrape_real_estate()