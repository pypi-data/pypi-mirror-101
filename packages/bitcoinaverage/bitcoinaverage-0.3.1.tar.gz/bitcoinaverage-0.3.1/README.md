# BitcoinAverage PIP Library

The following examples demonstrate how Http and Websocket requests are made.
Just enter your public key and you can run the examples.

Get your api key by logging in here: https://pro.bitcoinaverage.com/

Official documentation: https://apiv2.bitcoinaverage.com

More examples on Github: https://github.com/bitcoinaverage/api-integration-examples/

## Http example

```python
from bitcoinaverage import RestfulClient

if __name__ == '__main__':
    public_key = 'your_public_key'

    restful_client = RestfulClient(public_key)

    ticker_global_per_symbol = restful_client.ticker_global_per_symbol('BTCUSD')
    print('Global Ticker for BTCUSD:')
    print(ticker_global_per_symbol)
```

## Websocket V1 example

```python
from bitcoinaverage import TickerWebsocketClient

if __name__ == '__main__':
    public_key = 'your_public_key'

    print('Connecting to the ticker websocket...')
    ws = TickerWebsocketClient(public_key)
    ws.ticker_data('local', 'BTCUSD')
```

## Websocket V2 examples

Version 2 the websocket clients accept a list of cryptocurrencies and a list of exchange respectively.
They also use new optimized algorithm for quicker updates.


### Ticker

```python
from bitcoinaverage import TickerWebsocketClientV2

if __name__ == '__main__':
    public_key = 'your_public_key'

    print('Connecting to the ticker websocket...')
    ws = TickerWebsocketClientV2(public_key)
    ws.ticker_data('local', ['BTCUSD', 'ETHUSD'])
```

### Exchanges

```python

from bitcoinaverage import ExchangeWebsocketClientV2

if __name__ == '__main__':
    public_key = 'your_public_key'

    print('Connecting to the exchange websocket...')
    ws = ExchangeWebsocketClientV2(public_key)
    ws.exchange_data(['bitstamp', 'coinbasepro'])
```

#### Copyright Blockchain Data LTD