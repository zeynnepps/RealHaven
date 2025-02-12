import asyncio
import json
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from openai import OpenAI

SBR_WS_CDP = 'wss://brd-customer-hl_9720de3a-zone-real_estate:42c9d0uh6cag@brd.superproxy.io:9222'
BASE_URL = "https://www.zillow.com"
client = OpenAI(api_key="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")
LOCATION = "San Jose, CA"

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

    res = response.choices[0].message.content
    json_data = json.loads(res)

    return json_data

async def run(pw):
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)

    try:
        page = await browser.new_page()
        print(f'Connected! Navigating to {BASE_URL}')
        await page.goto(BASE_URL)

        # Wait for the search box to appear and enter the location
        await page.fill('input[placeholder="Enter an address, neighborhood, city, or ZIP code"]', LOCATION)
        await page.keyboard.press("Enter")
        print("Waiting for search results...")
        await page.wait_for_load_state("load")

        try:
            # Wait for the property list to become visible (using the proper selector)
            await page.wait_for_selector('article.list-card', state='visible', timeout=60000)
        except TimeoutError:
            print("Timeout error: Element 'article.list-card' not visible within 60 seconds.")
            return

        content = await page.inner_html('ul.listings')
        soup = BeautifulSoup(content, "html.parser")
        results = []

        # Use the updated selector for each listing
        for idx, div in enumerate(soup.find_all("article", class_="list-card")):
            link = div.find('a')['href']
            data = {
                "address": div.find('address').text if div.find('address') else "",
                "price": div.find(class_="list-card-price").text if div.find(class_="list-card-price") else "",
                "link": link if "http" in link else BASE_URL + link
            }

            print("Navigating to the listing page", data['link'])
            await page.goto(data['link'])
            await page.wait_for_load_state("load")

            # Wait for property details to load
            await page.wait_for_selector('div[data-testid="property-details"]', timeout=60000)
            content = await page.inner_html('div[data-testid="property-details"]')
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
