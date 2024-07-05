import ccxt
from utils.utilities import ccxt_ohlcv_to_df
from utils.strategies import BBStrategy
from utils.backtester import Backtester

if __name__ == '__main__':
  print('Backtester is starting...')

  exchange_id = 'binance'
  exchange_class = getattr(ccxt, exchange_id)
  exchange = exchange_class()

  ohclv = exchange.fetch_ohlcv('BTC/USDT', '1h', 1000)
  df = ccxt_ohlcv_to_df(ohclv)

  strategy = BBStrategy()
  strategy.setUp(df)

  tryback = Backtester()
  tryback.__backtesting__(df, strategy)
  report = tryback.report('BTC/USDT', '2021-01-01', '2021-12-31')
  print(report)
