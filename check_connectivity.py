import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for url in ["https://x.com", "https://gemini.google.com"]:
            try:
                await page.goto(url, timeout=30000)
                print(f"Successfully reached {url}")
            except Exception as e:
                print(f"Failed to reach {url}: {e}")
        await browser.close()

asyncio.run(check())
