import asyncio
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
#from openai import OpenAI

SBR_WS_CDP = 'wss://brd-customer-hl_41345ae3-zone-scraping_browser1:fabvcm73dd0u@brd.superproxy.io:9222'
BASE_URL = "https://www.zillow.com"
LOCATION = "San Jose, CA"

def extract_property_details(content):
    print("Extracting property details...")
    soup = BeautifulSoup(content, "html.parser")

    property_details = {
        "price": soup.find(attrs={"data-test": "property-card-price"}).text.strip() if soup.find(attrs={"data-test": "property-card-price"}) else "",
        "address": soup.find(attrs={"data-test": "address"}).text.strip() if soup.find(attrs={"data-test": "address"}) else "",
        "bedrooms": soup.find(attrs={"data-test": "bed-bath"}).text.split("•")[0].strip() if soup.find(attrs={"data-test": "bed-bath"}) else "",
        "bathrooms": soup.find(attrs={"data-test": "bed-bath"}).text.split("•")[1].strip() if soup.find(attrs={"data-test": "bed-bath"}) else "",
        "square_feet": soup.find(attrs={"data-test": "sqft"}).text.strip() if soup.find(attrs={"data-test": "sqft"}) else "",
        "year_built": soup.find(attrs={"data-test": "year-built"}).text.strip() if soup.find(attrs={"data-test": "year-built"}) else "",
        "property_type": soup.find(attrs={"data-test": "property-type"}).text.strip() if soup.find(attrs={"data-test": "property-type"}) else "",
        "lot_size": soup.find(attrs={"data-test": "lot-size"}).text.strip() if soup.find(attrs={"data-test": "lot-size"}) else "",
        "zestimate": soup.find(attrs={"data-test": "zestimate"}).text.strip() if soup.find(attrs={"data-test": "zestimate"}) else "",
        "hoa_fees": soup.find(attrs={"data-test": "hoa-fees"}).text.strip() if soup.find(attrs={"data-test": "hoa-fees"}) else "",
    }

    return property_details

async def run(pw):
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    print("Script started")

    try:
        page = await browser.new_page()
        print(f'Connected! Navigating to {BASE_URL}')
        await page.goto(BASE_URL)
        print("Page loaded:", page)

        # Wait for the search box to appear and enter the location
        await page.fill('input[placeholder="Enter an address, neighborhood, city, or ZIP code"]', LOCATION)
        await page.keyboard.press("Enter")
        print(f"Searching for properties in {LOCATION}...")
        await page.wait_for_load_state("load")

        try:
            await page.wait_for_selector('.StyledPropertyCard-c11n-8-106-0__sc-g2ckw9-0', state='visible', timeout=60000)
            print(f"Properties in {LOCATION} loaded successfully!")
        except TimeoutError:
            print(f"Timeout error: Could not find {LOCATION} listings!")
            return

        content = await page.inner_html('ul.StyledCarouselScrollContainer-c11n-8-106-0__sc-1jrjjf3-0', timeout=60000)
        soup = BeautifulSoup(content, "html.parser")
        results = []

        print(f"Searching for elements with selector: article.StyledPropertyCard-c11n-8-109-1__sc-g2ckw9-0")

        found_properties = soup.find_all("article", class_=lambda x: x and x.startswith('StyledPropertyCard'))
        print(f"Found {len(found_properties)} properties in {LOCATION}")

        for div in found_properties:
            link_tag = div.find('a')
            link = link_tag['href'] if link_tag else ""

            print(f"Link: {link}")

            address_tag = div.find(attrs={"data-test": "address"})
            address = address_tag.text.strip() if address_tag else ""
            print(f"Address: {address}")
            
            price_tag = div.find(attrs={"data-test": "property-card-price"})
            price = price_tag.text.strip() if price_tag else ""
            print(f"Price: {price}")

            # full_link = link if "http" in link else BASE_URL + link
            # print(f"Processing property: {address}, Link: {full_link}")

            data = {
                "address": address,
                "price": price,
                "link": link if "http" in link else BASE_URL + link
            }

            print(f"Data: {data}")

            try:
                print(f"Navigating to the listing page: {data['link']}")
                await page.goto(data['link'], timeout=120000)
                await page.wait_for_load_state("load")
                await page.wait_for_selector('[data-test="property-card"]', state='visible', timeout=60000)
            except Exception as e:
                print(f"Error navigating to {data['link']}: {e}")
                continue  # Skip this property if an error occurs

            content = await page.inner_html('[data-test="property-card"]')

            if content:
                print("Content found for the property!")
                property_details = extract_property_details(content)
                data.update(property_details)
                results.append(data)

        # Save the results to a file
        with open("output.json", "w") as f:
            json.dump(results, f, indent=4)
        print(f"Saved {len(results)} properties to output.json")

    finally:
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())