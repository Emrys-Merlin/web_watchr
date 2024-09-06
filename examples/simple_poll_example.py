from playwright.sync_api import Playwright
from web_watchr import Watchr
from web_watchr.compare import DummyComparer

watchr = Watchr(
    comparer=DummyComparer(),
)


@watchr.set_poller
def poll(playwright: Playwright) -> str:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.example.com/")
    text = page.get_by_role("heading").inner_text()

    # ---------------------
    context.close()
    browser.close()

    return text


if __name__ == "__main__":
    watchr()
