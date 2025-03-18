import asyncio
from playwright.async_api import async_playwright
import json
import pandas as pd

browser_url = 'your-key-here'

async def main():
    async with async_playwright() as pw:
        print('Connecting to remote browser...')
        browser = await pw.chromium.connect_over_cdp(browser_url)  # Connecting via proxy
        print('Launching browser with proxy...')
        page = await browser.new_page()
        
        print('Navigating to Zillow...')
        await page.goto('https://www.zillow.com/homes/for_sale/San-Jose_rb/', timeout=3600000)
        
        html = await page.content()
        with open("zillow_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Page saved. Check zillow_debug.html")

        # Wait for listings to load
        #await page.wait_for_selector('article.property-card', timeout=30000)  # Adjusted selector

        print('Scraping data...')
        listings = []
        
        # Selecting property cards
        properties = await page.query_selector_all('div.property-card-data')

        for property in properties:
            result = {}

            # Extract address
            address = await property.query_selector('address[data-test="property-card-addr"]')
            result['address'] = await address.inner_text() if address else 'N/A'

            # Extract price
            price = await property.query_selector('span[data-test="property-card-price"]')
            result['price'] = await price.inner_text() if price else 'N/A'

            # Extract bedrooms, bathrooms, and square footage
            details = await property.query_selector_all('ul.dmDolk > li')
            result['bedrooms'] = await details[0].inner_text() if len(details) >= 1 else 'N/A'
            result['bathrooms'] = await details[1].inner_text() if len(details) >= 2 else 'N/A'
            result['sqft'] = await details[2].inner_text() if len(details) >= 3 else 'N/A'

            # Extract home type
            type_div = await property.query_selector('div.gxlfal')
            result['type'] = (await type_div.inner_text()).split("-")[1].strip() if type_div else 'N/A'

            listings.append(result)

        # Close browser
        await browser.close()

        # **DEBUGGING: Print listings**
        print("Extracted Listings:", listings)

        # Save to JSON
        with open('listings-brightdata.json', 'w') as f:
            json.dump(listings, f, indent=4)
        print('Data written to JSON file')

        # Save to CSV
        df = pd.DataFrame(listings)
        df.to_csv('listings-brightdata.csv', index=False)
        print('Data written to CSV file')

        return listings

# Run async function
listings = asyncio.run(main())
