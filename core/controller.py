from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self):
        self.pw = None
        self.browser = None
        self.page = None

    async def launch(self):
        self.pw = await async_playwright().start()
        # 'chrome' channel uses the installed Google Chrome on your Mac
        self.browser = await self.pw.chromium.launch(headless=False, channel="chrome")
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        return self.page

    async def shutdown(self):
        if self.browser:
            await self.browser.close()
        if self.pw:
            await self.pw.stop()