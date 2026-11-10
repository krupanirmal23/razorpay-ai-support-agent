import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1200,'height':100},device_scale_factor=2)
        await pg.goto('file:///workspace/portfolio/razorpay-ai-agent/docs/build/chart.html'); await pg.wait_for_timeout(400)
        h=await pg.evaluate('document.body.scrollHeight'); await pg.set_viewport_size({'width':1200,'height':h})
        await pg.screenshot(path='chart.png'); await b.close()
asyncio.run(main())
