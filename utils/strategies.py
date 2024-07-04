import pandas_ta as ta
from utils.utilities import ccxt_ohlcv_to_df


class BBStrategy:
  def __init__(self, bb_len=20, n_std=20, rs_len=14, rsi_overbought=60, rsi_oversold=40) -> None:
    self.bb_len = bb_len
    self.n_std = n_std
    self.rs_len = rs_len
    self.rsi_overbought = rsi_overbought
    self.rsi_oversold = rsi_oversold


  def setUp(self, df):
    bb = ta.bbands(df["close"], length=self.bb_len, std=self.n_std)
    df["bb_lowerband"] = bb.iloc[:, 0]
    df["bb_middleband"] = bb.iloc[:, 1]
    df["bb_upperband"] = bb.iloc[:, 2]
    df["rsi"] = ta.rsi(df["close"], length=self.rs_len)
    self.datframe = df

  def checkLongSignal(self, i=None):
    df = self.datframe

    if i is None:
      i = len(df)

    if (df['rsi'].iloc[i] < self.rsi_overbought) and \
        (df['rsi'].iloc[i] > self.rsi_oversold) and \
        (df['low'].iloc[i-1] < df['bb_lowerband'].iloc[i-1]) and \
        (df['low'].iloc[i] < df['bb_lowerband'].iloc[i]):
      return True
    
    return False
  
  def checkShortSignal(self, i=None):
    df = self.datframe

    if i is None:
      i = len(df)

    if (df['rsi'].iloc[i] < self.rsi_overbought) and \
        (df['rsi'].iloc[i] > self.rsi_oversold) and \
        (df['high'].iloc[i-1] > df['bb_upperband'].iloc[i-1]) and \
        (df['high'].iloc[i] < df['bb_upperband'].iloc[i]):
      return True
    
    return False
