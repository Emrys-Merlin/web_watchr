![GitHub License](https://img.shields.io/github/license/Emrys-Merlin/web_watchr)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FEmrys-Merlin%2Fweb_watchr%2Fmain%2Fpyproject.toml)

| 3.10 | 3.11 | 3.12 | 3.13 |
|------|------|------|------|
|![tests](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FEmrys-Merlin%2Fec2e4e339a048ca0f0b996517d282a4a%2Fraw%2Fweb_watchr_3.10-junit-tests.json)|![tests](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FEmrys-Merlin%2Fec2e4e339a048ca0f0b996517d282a4a%2Fraw%2Fweb_watchr_3.11-junit-tests.json)|![tests](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FEmrys-Merlin%2Fec2e4e339a048ca0f0b996517d282a4a%2Fraw%2Fweb_watchr_3.12-junit-tests.json)|![tests](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FEmrys-Merlin%2Fec2e4e339a048ca0f0b996517d282a4a%2Fraw%2Fweb_watchr_3.13-junit-tests.json)|
|![Endpoint Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Emrys-Merlin/ec2e4e339a048ca0f0b996517d282a4a/raw/web_watchr_3.10-cobertura-coverage.json)|![Endpoint Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Emrys-Merlin/ec2e4e339a048ca0f0b996517d282a4a/raw/web_watchr_3.11-cobertura-coverage.json)|![Endpoint Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Emrys-Merlin/ec2e4e339a048ca0f0b996517d282a4a/raw/web_watchr_3.12-cobertura-coverage.json)|![Endpoint Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/Emrys-Merlin/ec2e4e339a048ca0f0b996517d282a4a/raw/web_watchr_3.13-cobertura-coverage.json)|

# WebWatchr

This python package is a framework around [Playwright](https://Playwright.dev/python) to monitor a website and receive an alert if the monitored text changes. The setup is quite modular. To specify the website to monitor, you need to define a `Callable[[Playwright], str]` which is responsible to extract the text you are interested in. Currently, the only available alerting channel is via [telegram](https://telegram.org) bot. However, more alerting channels will follow.

> [!IMPORTANT]
> Before you start scraping any website, please make sure that you are allowed to. Besides legal obligations, please consider reaching out to the website owner and please respect `robots.txt`files.

## Installation

The package is available via PyPI. You can install it via
```
pip install web_watchr
```
If you prefer the latest changes, you can also install it directly from the repository via:
```
pip install git+https://github.com/Emrys-Merlin/web_watchr
```

## Usage

After the installation, the intended way to invoke the framework is by writing a small runner script (which you can find [here](examples/simple_dummy_example.py)):
```Python
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
    context.close()
    browser.close()

    return text


if __name__ == "__main__":
    watchr()
```

The runner consists of three parts:

1. A new `Watchr` object is initialized. For illustration purposes, a `DummyComparer` instance is passed to it, which will indicate that the monitored text has changed no matter the input.
2. We implement the `poll` function and decorate it with `@watchr.set_poller`. The poll function contains all the website-specific logic to extract the text of interest. Most of this function can be automatically generated using [`playwright codegen`](https://playwright.dev/python/docs/codegen#running-codegen).
3. We invoke `watchr`, which will poll the website once.

By default, `watchr` will simply print the text to std out. If you want to receive alerts on your phone via telegram, we need to modify the [script](examples/simple_telegram_alerting.py) slightly:
```Python
import os

from playwright.sync_api import Playwright
from web_watchr import Watchr
from web_watchr.alert import TelegramAlerter

watchr = Watchr(
    alerter=TelegramAlerter(
        token=os.getenv("TELEGRAM_TOKEN"),
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
    )
)


@watchr.set_poller
def poll(playwright: Playwright) -> str:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.example.com/")
    text = page.get_by_role("heading").inner_text()
    context.close()
    browser.close()

    return text


if __name__ == "__main__":
    watchr()
```

There are two key changes compared to the inital script:

1. We removed the `DummyComparer`. By default, `Watchr` uses an `FSComparer` which stores the old state in a file. The default location is `~/.local/share/web_watchr/cache`, which can be adapted. This has the advantage that the runner does not need to run continously, but can be invoked periodically (e.g., via `cron`).
2. We instantiated a `TelegramAlerter` reading a `token` and a `chat_id` from some environment variables. These are secrets of your bot that you need to send messages with it. If you are unsure how to create a bot, please have a look [here](https://core.telegram.org/bots/tutorial#obtain-your-bot-token). To find out your `chat_id`, you can use the approach mentioned [here](https://stackoverflow.com/a/32572159/9685500).

> [!CAUTION]
> Keep your bot token secret. In particular, make sure to never add it to version control. Otherwise, malicious actors can use it for ther purposes.

Running the script will now send updates to your phone via telegram!

## Documentation

So far, almost all of the documentation is restricted to this readme. However, you can have a look at the [API Reference](https://emrys-merlin.github.io/web_watchr/api).

## Contribution

If you like what you see and would like to extend it, you can do so by
- filing an issue with a feature request (no promises on my part though) and
- forking the repo and opening a pull request.

I'm always happy to chat, so you can also simply reach out and we can talk.
