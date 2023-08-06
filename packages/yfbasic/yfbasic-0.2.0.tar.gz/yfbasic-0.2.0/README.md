yfbasic
=======

A thin python wrapper to retrieve price action data from the Yahoo! finance API.

There are similar packages available that does this, most notably
[yfinance](https://github.com/ranaroussi/yfinance). The purpose of this package
is to present the raw data as typed objects to be consumed as desired.

# Getting started

The interface is straight forward, just import and query.

``` python
import yfbasic

data = yfbasic.query("GME")
```

The supporting parameters are typed as well.

``` python
import yfbasic
from yfbasic import Range, Interval

data = yfbasic.query("GME", range=Range.r1mo, interval=Interval.i1h)
```

You can use `query_threaded` to parallelise the data retrieval.

``` python
import yfbasic

symbols = ("GME", "AMC", "TSLA")

data = yfbasic.query_threaded(symbols)
```

# Working with the data

The data is modelled directly of the structure returned by the yahoo api. This
makes it a bit more low level to work with, but the package makes no presumptions about
how you intend to work with the data.

The best way to understand the data is to look at the [data structure](yfbasic/models/chart.py)
directly.

## Error handling

If we look at the `Chart` data model it contains two optional parameters, 
`result` and `error` which means we need to do application side checking of the
data. To satisfy type safety we need to at least verify the existence of
results by checking `data.chart.results` . If we want insight into any API side
errors we could verify and action upon `data.chart.error`

``` python
import yfbasic

data = yfbasic.query("GME")

# verifying the API produced results.
if data.chart.result:
    result = data.chart.result[0]
    quotes = result.indicators.quote[0]

    # getting price action data
    timestamps = result.timestamp
    open = quotes.open
    close = quotes.close
    high = quotes.high
    low = quotes.low
    volume = quotes.volume
```
