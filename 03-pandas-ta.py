import ccxt
import pandas_ta as ta
from utils.utilities import ccxt_ohlcv_to_df

if __name__ == "__main__":
  exchange_id = 'binance'
  exchange_class = getattr(ccxt, exchange_id)
  exchange = exchange_class()

  ohclv = exchange.fetch_ohlcv('BTC/USDT', '1h')
  df = ccxt_ohlcv_to_df(ohclv)

  df.ta.cores = 2
  emastrategy = ta.Strategy(
      name="EMA Strategy",
      ta=[
          {"kind": "ema", "length": 8},
          {"kind": "ema", "length": 21},
      ]
  )

  df.ta.strategy(ta.CommonStrategy)

  print('\nBinance data')
  print(df)