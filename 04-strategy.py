import ccxt
from utils.utilities import ccxt_ohlcv_to_df
from utils.strategies import BBStrategy

if __name__ == "__main__":
  exchange_id = 'binance'
  exchange_class = getattr(ccxt, exchange_id)
  exchange = exchange_class()

  ohclv = exchange.fetch_ohlcv('BTC/USDT', '30m', 1000)
  df = ccxt_ohlcv_to_df(ohclv)

  strategy = BBStrategy()
  strategy.setUp(df)

  count = 0
  for i in range(len(df)):
    result = strategy.checkLongSignal(i)
    if result:
      count += 1

  print(f"Long signals: {count}")