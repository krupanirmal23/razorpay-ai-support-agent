import asyncio,glob
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':900},device_scale_factor=2)
        for f in sorted(glob.glob('0*.html')):
            await pg.set_viewport_size({'width':1440,'height':560 if f.startswith('04') else 900}); await pg.goto('file:///workspace/portfolio/razorpay-ai-agent/mockups/'+f); await pg.wait_for_timeout(600)
            await pg.screenshot(path=f.replace('.html','.png')); print(f)
        await b.close()
asyncio.run(main())
