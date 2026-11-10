import sys, asyncio, re
from playwright.async_api import async_playwright
pages = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width':1366,'height':860}, user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36', locale='en-IN')
        for name,url in pages:
            pg = await ctx.new_page()
            try:
                r = await pg.goto(url, wait_until='domcontentloaded', timeout=45000)
                await pg.wait_for_timeout(4000)
                for sel in ['button:has-text("Accept")','button:has-text("Got it")','button:has-text("Allow")','button:has-text("OK")']:
                    try: await pg.click(sel, timeout=800)
                    except: pass
                await pg.screenshot(path=f'teardown/screens/{name}.png')
                txt = await pg.inner_text('body')
                open(f'teardown/text/{name}.txt','w').write(f'URL: {url}\nFINAL: {pg.url}\nSTATUS: {r.status if r else None}\n\n'+txt)
                print(name, r.status if r else None, pg.url, len(txt))
            except Exception as e: print(name,'ERR',str(e)[:120])
            await pg.close()
        await b.close()
asyncio.run(main())
