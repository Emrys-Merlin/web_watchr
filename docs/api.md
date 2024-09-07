# API Reference

The WebWatchr consists of three parts.

1. `web_watchr`: This module contains the [`web_watchr.Watchr`][] class that orchestrates the whole polling, comparing, and alerting.
2. `web_watchr.compare`: This module contains classes that can be used to check if the state has changed. If you want to implement your own comparer, you need to inherit from [`web_watchr.compare.AbstractComparer`][].
3. `web_watchr.alert`: This module contains classes that can be used to send out alerts of a new state. If you want to implement your own comparer, you need to inherit from [`web_watchr.alert.AbstractAlerter`][].


## web_watchr

::: web_watchr.Watchr

<br>
## web_watchr.compare

::: web_watchr.compare.Status

<br>
::: web_watchr.compare.AbstractComparer

<br>
::: web_watchr.compare.DummyComparer

<br>
::: web_watchr.compare.FSComparer

<br>
## web_watchr.alert

::: web_watchr.alert.AbstractAlerter

<br>
::: web_watchr.alert.PrintAlerter

<br>
::: web_watchr.alert.TelegramAlerter
