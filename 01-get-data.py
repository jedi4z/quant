import ccxt

print(ccxt.exchanges)

exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class()

symbol = 'BTC/USDT'
timeframe = '1h'

binance_ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

print('\nBinance data')
print(binance_ohlcv[0])