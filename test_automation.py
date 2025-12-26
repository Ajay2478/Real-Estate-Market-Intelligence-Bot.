from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("🚀 Starting the Browser Bot...")
# This step automatically downloads the driver that matches your Chrome version
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")
print(f"✅ Connection Successful! Page Title: {driver.title}")

time.sleep(5) # Keeps the window open for 5 seconds so you can see it
driver.quit()
print("🤖 Test complete. Your system is ready for Project 2!")