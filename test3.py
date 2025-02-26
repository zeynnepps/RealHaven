from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening a browser
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Redfin Listings Page
url = "https://www.redfin.com/city/17420/CA/San-Jose"
driver.get(url)

# Wait for JavaScript to load (increase if needed)
time.sleep(7)

# Get the page source after JavaScript executes
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

with open("debug.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())  # Save page HTML for debugging
# Extract Data from Listings

data = []
listings = soup.find_all("div", {"class": "HomeCardsContainer"})  # Update selector if needed

for listing in listings:
    price_elem = listing.find("span", {"class": "homecardV2Price"})
    address_elem = listing.find("span", {"class": "collapsedAddress"})

    price = price_elem.get_text(strip=True) if price_elem else "N/A"
    address = address_elem.get_text(strip=True) if address_elem else "N/A"

    data.append({"price": price, "address": address})

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("real_estate_data.csv", index=False)

# Close the driver
driver.quit()
print("Scraping completed. CSV file saved.")
