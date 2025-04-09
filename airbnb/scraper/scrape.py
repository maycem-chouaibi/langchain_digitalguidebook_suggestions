import asyncio
import random
import json
import os
import time
from typing import List, Dict, Any
from playwright.async_api import async_playwright, BrowserContext, Page, Response
from clean_data import parse_data
from consts import *
from format_details import *


async def scroll_until_request(page: Page, sections: dict, 
                               max_attempts: int = 20, scroll_delay: int = 2000) -> List[Dict]:
    results = {}
    found_sections = set()
    response_future = asyncio.Future()
    
    await page.wait_for_selector('button[aria-label="Close"]', timeout=10000)
    await page.click('button[aria-label="Close"]')
    
    async def handle_response(response: Response):
        if response.ok:
            for section_name, section in sections.items():
                if section in response.url and section not in found_sections:
                    try:
                        body = await response.json()
                        if section_name == "generalInfo":
                            listing_data = search_key(body, "stayListingData")
                            if not listing_data or listing_data == {} or listing_data is None:
                                print(f"⚠️ Empty staysListingData in generalInfo response, skipping...")
                                continue
                        cleaned_response = process_json(body, section_name)
                        results[section_name] = cleaned_response

                        found_sections.add(section)
                        
                        if len(found_sections) == len(sections) and not response_future.done():
                            response_future.set_result(True)
                    except Exception as e:
                        print(f"⚠️ Error fetching response body: {e}")
    
    page.on("response", lambda response: asyncio.create_task(handle_response(response)))
    
    await page.wait_for_load_state("networkidle", timeout=30000)
    
    print("Performing initial actions to load top section...")
    
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(1000)
    
    await page.reload(wait_until="networkidle")
    await page.wait_for_timeout(2000)
    
    try:
        top_elements = await page.query_selector_all("header *, nav *, .header *, .navigation *, .top *")
        for el in top_elements[:2]:
            await el.hover()
            await page.wait_for_timeout(500)
    except Exception as e:
        print(f"Couldn't hover top elements: {e}")
    
    try:
        tabs = await page.query_selector_all("nav button, .tabs button, .tab, [role=tab]")
        for tab in tabs[:3]:  # First 3 tabs
            await tab.click()
            await page.wait_for_timeout(1000)
    except Exception as e:
        print(f"Couldn't click tab elements: {e}")
    
    attempts = 0
    await page.wait_for_load_state("networkidle")
    while len(found_sections) < len(sections) and attempts < max_attempts:
        print(f"🔄 Scrolling... Attempt {attempts + 1}/{max_attempts}. Found {len(found_sections)}/{len(sections)} sections")
        await page.mouse.wheel(0, 4000)
        
        try:
            await asyncio.wait_for(asyncio.shield(response_future), timeout=scroll_delay/1000)
            print(f"✅ Found all {len(sections)} required sections")
            break
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            print(f"Error during scrolling: {e}")
            
        attempts += 1
        
    if len(found_sections) < len(sections):
        print(f"⚠️ Only found {len(found_sections)}/{len(sections)} sections after {max_attempts} attempts")
        print(f"Missing sections: {set(sections) - found_sections}")

    return results

async def get_listing_links(context: BrowserContext, city: str, checkin: str, checkout: str) -> List[str]:
    page = await context.new_page()
    search_url = AIRBNB_URL.format(city=city, checkin=checkin, checkout=checkout)
    
    listing_links = set()
    
    try:
        await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(random.randint(3000, 5000))
        
        i = 0
        # while True:
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
                # break
                
            await next_button.click()
            await page.wait_for_timeout(random.randint(2000, 4000))
            await page.wait_for_function("() => document.readyState === 'complete'")
            
        except Exception as e:
            print(f"Error processing page {i+1}: {e}")
            # break
        # i += 1
    finally:
        try:
            await page.close()
            print("")
        except Exception as e:
            print(f"Error closing page: {e}")
        
    print(f"Found total of {len(listing_links)} unique listings")
    return list(listing_links)

async def process_single_listing(context: BrowserContext, url: str, sections: List[str]) -> Dict:
    listing_id = url.split("/")[-1]
    print(f"Processing listing: {listing_id} - {url}")
    
    page = await context.new_page()
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        results = await scroll_until_request(page, sections)
        
        listing_data = {
            "listing_id": listing_id,
            "url": url,
            "scraped_at": time.time(),
            "data": results
        }
        
        filename = f"{listing_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(listing_data, f, indent=2)
        
        print(f"✅ Saved listing {listing_id} to {filename}")
        return listing_data
        
    except Exception as e:
        print(f"Error processing listing {listing_id}: {e}")
        return {"listing_id": listing_id, "url": url, "error": str(e)}
    finally:
        try:
            await page.close()
            print()
        except Exception as e:
            print(f"Error closing page for listing {listing_id}: {e}")

async def scrape():
    city = "Marrakech"
    checkin = "2025-05-01"
    checkout = "2025-05-02"
    
    playwright = None
    browser = None
    summary_file = f"{city.lower().replace(' ', '_')}_summary.json"

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
            
        all_results = []
        for url in urls[:1]:
            await asyncio.sleep(random.uniform(2, 4))
            result = await process_single_listing(context, url, API_ENDPOINTS)
            all_results.append(result)
        
        summary_data = {
            "city": city,
            "checkin": checkin,
            "checkout": checkout,
            "total_listings": len(all_results),
            "listings": [{"id": item.get("listing_id"), "url": item.get("url")} for item in all_results]
        }
        
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"Scraping complete! {len(all_results)} listings saved!")
        print(f"Summary saved to {summary_file}")
        
        await asyncio.sleep(3)
        
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

    return summary_file

if __name__ == '__main__':
    summary_file = asyncio.run(scrape())
    parse_data(summary_file)


