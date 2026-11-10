import asyncio
from playwright.async_api import async_playwright
jobs=[('rzp_hold_section','https://razorpay.com/docs/payments/settlements/dashboard/','Enable Settlements Placed On Hold'),
('rzp_states_section','https://razorpay.com/docs/payments/set-up/','Account States'),
('rzp_escalate_section','https://razorpay.com/docs/payments/dashboard/support/','Escalate a Support Ticket'),
('rzp_settle_cycle','https://razorpay.com/docs/payments/settlements/faqs/','What is the settlement cycle you offer'),
('cf_settle_section','https://www.cashfree.com/docs/help/payments/settlements/settlements','My Settlement isn'),
('cf_contact_section','https://www.cashfree.com/docs/help/overview','Contact support')]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1366,'height':860},device_scale_factor=1)
        for name,url,txt in jobs:
            try:
                await pg.goto(url,wait_until='domcontentloaded',timeout=60000); await pg.wait_for_timeout(5000)
                loc=pg.get_by_text(txt).first
                await loc.scroll_into_view_if_needed(timeout=10000)
                try: await loc.click(timeout=3000)  # opens accordions
                except: pass
                await pg.wait_for_timeout(1200)
                await pg.evaluate("(t)=>{const el=[...document.querySelectorAll('h1,h2,h3,summary,button,div,span')].find(e=>e.innerText&&e.innerText.trim().startsWith(t)); if(el){const y=el.getBoundingClientRect().top+window.scrollY-110; window.scrollTo(0,y);}}",txt)
                await pg.wait_for_timeout(1200)
                await pg.screenshot(path=f'teardown/screens/{name}.png'); print('ok',name)
            except Exception as e: print('ERR',name,str(e)[:100])
        await b.close()
asyncio.run(main())
