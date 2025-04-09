import asyncio
import random
import json
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.async_api import async_playwright, BrowserContext, Page, Response
from consts import *
from browser_use import Agent, Browser, BrowserConfig, BrowserContextConfig
from browser_use.browser.context import BrowserContext

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def get_listing_links(context: BrowserContext, city: str, checkin: str, checkout: str) -> List[str]:
    page = await context.new_page()
    search_url = AIRBNB_URL.format(city=city, checkin=checkin, checkout=checkout)
    
    listing_links = set()
    
    try:
        await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(random.randint(3000, 5000))
        
        i = 0
        while True:
            try:
                await page.wait_for_selector("a[href*='/rooms/']", timeout=10000)
                listing_elements = await page.query_selector_all("a[href*='/rooms/']")
                
                current_page_links = []
                for elem in listing_elements:
                    href = await elem.get_attribute("href")
                    if href and "/rooms/" in href:
                        full_url = f"https://www.airbnb.com{href.split('?')[0]}"
                        if full_url not in listing_links:
                            current_page_links.append(full_url)
                            listing_links.add(full_url)
                
                print(f"Page {i+1}: Found {len(current_page_links)} new listings (total: {len(listing_links)})")
                
                next_button = await page.query_selector("a[aria-label='Next']")
                if not next_button:
                    print("No more pages available")
                    break
                    
                await next_button.click()
                await page.wait_for_timeout(random.randint(2000, 4000))
                await page.wait_for_function("() => document.readyState === 'complete'")
                i += 1    
            except Exception as e:
                print(f"Error processing page {i+1}: {e}")
            break
        
    finally:
        try:
            await page.close()
        except Exception as e:
            print(f"Error closing page: {e}")
        
    print(f"Found total of {len(listing_links)} unique listings")
    return list(listing_links)

async def brawser_use_llm():
    return

async def scrape():
    city = "Marrakech"
    checkin = "2025-05-01"
    checkout = "2025-05-02"
    
    playwright = None
    browser = None
    
    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 2000, "height": 1000},
            java_script_enabled=True,
            locale="en-US"
        )

        print(f"Searching for listings in {city} ({checkin} to {checkout})...")
        urls = await get_listing_links(context, city, checkin, checkout)
        if not urls:
            print("No listings found!")
            return
        return urls
        
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        print("Cleaning up resources...")
        
        if browser:
            try:
                await browser.close()
                print("Browser closed")
            except Exception as e:
                print(f"Error closing browser: {e}")
                
        if playwright:
            try:
                await playwright.stop()
                print("Playwright stopped")
            except Exception as e:
                print(f"Error stopping playwright: {e}")

async def extract_data(urls):
    browser_config = BrowserConfig(
        headless=False,
        disable_security=True
    )
    context_config = BrowserContextConfig(
                            wait_for_network_idle_page_load_time=3.0,
                            browser_window_size={'width': 2000, 'height': 1500},
                            minimum_wait_page_load_time=0.7,
                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
                            highlight_elements=True,
                            save_recording_path="results"
                            )
    browser = Browser(config=browser_config)
    context = BrowserContext(browser=browser, config=context_config)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, max_retries=2, api_key=GEMINI_API_KEY)

    for url in urls:
        initial_actions = [
            {"open_tab": {"url": "https://www.google.com"}},
            {"open_tab": {"url": url}},
            {"scroll_down": {"amount": 2000}}
        ]
    
        async with await browser.new_context() as context:
            agent = Agent(
                task="""
                    ## Primary Objective
                    You are a sophisticated data extraction and transformation assistant specialized in processing raw Airbnb scraped data. Your goal is to convert unstructured web scraping data into clean, organized, and analysis-ready database tables.

                    ## Data Processing Guidelines

                    ### 1. Input Validation
                    - Verify the integrity and completeness of the scraped Airbnb data
                    - Check for missing values, inconsistent formatting, and potential scraping artifacts
                    - Standardize data types and formats across all extracted information

                    ### 2. Table Schema Design
                    Create the following structured tables from the scraped data:

                    #### A. Listings Table
                    Columns:
                    - listing_id (unique identifier)
                    - host_id
                    - property_type
                    - room_type
                    - neighborhood
                    - city
                    - country
                    - latitude
                    - longitude
                    - total_occupancy
                    - bedrooms
                    - bathrooms
                    - bed_type
                    - amenities (JSON/array format)

                    #### B. Pricing Table
                    Columns:
                    - listing_id
                    - base_price
                    - cleaning_fee
                    - service_fee
                    - weekly_discount
                    - monthly_discount
                    - currency
                    - price_per_night
                    - minimum_stay

                    #### C. Availability Table
                    Columns:
                    - listing_id
                    - date
                    - is_available
                    - booking_status
                    - minimum_nights
                    - maximum_nights

                    #### D. Review Table
                    Columns:
                    - listing_id
                    - review_id
                    - reviewer_id
                    - reviewer_name
                    - review_date
                    - review_text
                    - rating_cleanliness
                    - rating_communication
                    - rating_checkin
                    - rating_accuracy
                    - rating_location
                    - rating_value

                    #### E. Host Table
                    Columns:
                    - host_id
                    - host_name
                    - host_since
                    - host_location
                    - host_response_rate
                    - host_response_time
                    - host_is_superhost
                    - host_listings_count

                    ## Data Cleaning Processes
                    1. Normalize text fields (trim whitespaces, convert to proper case)
                    2. Handle currency conversions if multiple currencies are present
                    3. Standardize date formats (YYYY-MM-DD)
                    4. Remove duplicate entries
                    5. Validate and correct geographical coordinates

                    ## Advanced Extraction Requirements
                    - Extract nested or complex JSON/nested data structures
                    - Handle multilingual listings and descriptions
                    - Identify and flag potentially suspicious or fraudulent listings

                    ## Output Specifications
                    - Provide data in CSV, JSON, or SQLite database format
                    - Include a comprehensive metadata file describing schema, data sources, and extraction timestamp
                    - Generate data quality report highlighting:
                    * Total records processed
                    * Percentage of complete vs. incomplete records
                    * Any data inconsistencies or anomalies detected

                    ## Error Handling
                    - Log all data extraction and transformation errors
                    - Provide detailed error messages for manual review
                    - Implement fallback mechanisms for incomplete or malformed data entries

                    ## Performance Optimization
                    - Use efficient parsing algorithms
                    - Minimize memory consumption
                    - Support batch processing for large datasets

                    ## Compliance and Privacy
                    - Anonymize personal identifiable information (PII)
                    - Ensure compliance with web scraping terms of service
                    - Respect data privacy regulations

                    ## Final Deliverable
                    Produce a comprehensive, clean, and structured dataset ready for further analysis, visualization, and machine learning applications.

                    ---

                    ### Usage Instructions
                    1. Input raw Airbnb scraping data
                    2. Apply the defined extraction and transformation rules
                    3. Validate and clean the extracted information
                    4. Generate structured output tables
                    5. Produce metadata and data quality report
                    """,
                initial_actions=initial_actions,
                llm=llm,
                browser_context=context
            )
            return await agent.run(max_steps=10)

if __name__=="__main__":
    import asyncio
    urls = asyncio.run(scrape())
    asyncio.run(extract_data(urls))