import asyncio
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from openai import OpenAI

SBR_WS_CDP = 'wss://brd-customer-hl_41345ae3-zone-scraping_browser1:fabvcm73dd0u@brd.superproxy.io:9222'
BASE_URL = "https://www.zillow.com"
client = OpenAI(api_key="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")
LOCATION = "San Jose, CA"
#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

def extract_property_details(input):
    print("Extracting property details...")
    command = """
        You are a data extractor model and you have been tasked with extracting information about the apartment for me into json.
        Here is the div for the property details:
        
        {input_command}
        
        this is the final json structure expected:
        {{
            "price": "",
            "address": "",
            "bedrooms": "",
            "bathrooms": "",
            "square_feet": "",
            "year_built": "",
            "property_type": "",
            "lot_size": "",
            "zestimate": "",
            "hoa_fees": ""
        }}
    """.format(input_command=input)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": command
        }]
    )
    print(f"Raw response: {response}")
    res = response.choices[0].message.content
    print(f"Processed content: {res}")
    json_data = json.loads(res)
    return json_data

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

        # current_url = page.url
        # print(f"Current URL after search: {current_url}")
        # if "san-jose" not in current_url.lower():
        #     print("The search page did not load with San Jose, CA. Exiting.")
        #     return
        
        try:
            # Wait for the property list to become visible (using the proper selector)
            await page.wait_for_selector('.StyledPropertyCard-c11n-8-106-0__sc-g2ckw9-0', state='visible', timeout=60000)
            print(f"Properties in {LOCATION} loaded successfully!")
        except TimeoutError:
            print(f"Timeout error: Could not find San Jose listings!")
            return

        content = await page.inner_html('ul.StyledCarouselScrollContainer-c11n-8-106-0__sc-1jrjjf3-0', timeout=60000)
        #print(content)
        soup = BeautifulSoup(content, "html.parser")
        results = []

        # Use the updated selector for each listing
        #StyledPropertyCard-c11n-8-106-0__sc-g2ckw9-0 jxPojq

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

            # if "San Jose" not in address:
            #     print(f"Skipping property: {address} (Not in San Jose)")
            #     continue

            data = {
                "address": address,
                "price": price,
                "link": link if "http" in link else BASE_URL + link
            }
            
            print(f"Data: {data}")

            print(f"Navigating to the listing page: {data['link']}")
            await page.goto(data['link'], timeout=120000)
            await page.wait_for_load_state("load")
            await page.wait_for_selector('[data-test="property-card"]', state='visible', timeout=60000)
            content = await page.inner_html('[data-test="property-card"]')


            if content:
                print("Content found for the property!")
                soup = BeautifulSoup(content, "html.parser")

                # Extract property details
                property_details = extract_property_details(content)
                data.update(property_details)
                results.append(data)

        # Save the results to a file
        with open("output.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Data saved to output.json")

    finally:
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())
