import asyncio
import json
import random

from bs4 import BeautifulSoup
from openai import OpenAI
from playwright.async_api import async_playwright

# 🔹 Bright Data Scraping Browser WebSocket
SBR_WS_CDP = 'your-key-here'
ZILLOW_URL = "https://www.zillow.com"
client = OpenAI(api_key="your-openai-apikey-here")
LOCATION = "San Jose, CA" 

def extract_property_details(input):
    print("Extracting property details...")
    command = f"""
        You are a data extractor model, and you need to extract property details into JSON format.
        Here is the raw HTML content of the property details section:

        {input}

        Please return JSON in the following format:
        {{
            "price": "",
            "address": "",
            "bedrooms": "",
            "bathrooms": "",
            "square_feet": "",
            "property_type": "",
            "year_built": "",
            "lot_size": "",
            "zillow_estimate": "",
            "monthly_HOA": ""
        }}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": command}]
    )

    res = response.choices[0].message.content
    json_data = json.loads(res)

    return json_data


async def scrape_zillow(playwright):
    print(f'Connecting to Bright Data Scraping Browser: {SBR_WS_CDP}')
    browser = await playwright.chromium.connect_over_cdp(SBR_WS_CDP)

    try:
        page = await browser.new_page()
        print(f'Connected! Navigating to {ZILLOW_URL}')
        await page.goto(ZILLOW_URL, timeout=60000)

        # 🔹 Enter location in Zillow search box
        print("Waiting for search box...")
        await page.wait_for_selector('input[placeholder="Enter an address, neighborhood, city, or ZIP code"]', timeout=10000)

        await page.fill('input[placeholder="Enter an address, neighborhood, city, or ZIP code"]', LOCATION)
        await page.keyboard.press("Enter")
        print(f"Searching for properties in {LOCATION}...")

        await asyncio.sleep(random.uniform(8, 12))  # Zillow needs extra time to load data
        await page.wait_for_selector('.StyledPropertyCard-c11n-8-106-0__sc-g2ckw9-0', state='visible', timeout=60000)

        print("Scrolling to load more listings...")
        for i in range(5):  # Scroll 5 times to ensure data loads
            print(f"Scrolling {i+1}/5...")
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(3)

        # 🔹 Extract property listing links
        print("Extracting property listings...")
        content = await page.content()
        print("🔹 PAGE CONTENT AFTER LOADING 🔹")
        print(content[:3000])
        soup = BeautifulSoup(content, "html.parser")


        # property_listings = soup.find_all("article", {"data-testid": "property-card"})
        # property_listings = soup.find_all("div", {"class": "property-card"})
        property_listings = soup.find_all("article", class_=lambda x: x and x.startswith('StyledPropertyCard'))
        if not property_listings:
            print("No properties found. Check the page structure or increase the sleep time.")
            return

        results = []

        for idx, listing in enumerate(property_listings):
            link_tag = listing.find("a", {"data-testid": "property-card-link"})
            if not link_tag:
                continue

            link = ZILLOW_URL + link_tag["href"]
            address = listing.find("address").text if listing.find("address") else "Unknown Address"
            price = listing.find("span", {"data-testid": "property-card-price"}).text if listing.find("span", {"data-testid": "property-card-price"}) else "Unknown Price"

            data = {"address": address, "price": price, "link": link}
            print(f"Scraped: {data}")

            results.append(data)

            # Save data incrementally
            with open("zillow_listings.json", "w") as f:
                json.dump(results, f, indent=4)

        print(f"✅ Scraped {len(results)} properties. Data saved to zillow_listings.json")

            # await page.goto(link)
            # await page.wait_for_load_state("load")
            # await asyncio.sleep(3)

            # details_content = await page.content()
            # details_soup = BeautifulSoup(details_content, "html.parser")

            # property_details = extract_property_details(str(details_soup))
            # data.update(property_details)


    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await scrape_zillow(playwright)


if __name__ == '__main__':
    asyncio.run(main())