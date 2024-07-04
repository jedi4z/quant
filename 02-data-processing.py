import pandas as pd
import ccxt

def ccxt_ohlcv_to_df(ohlcv):
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class()
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h')
df = ccxt_ohlcv_to_df(ohlcv)

print('\nBinance data')
print(df.head())

