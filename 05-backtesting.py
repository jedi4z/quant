import numpy as np
import ccxt
from utils.utilities import ccxt_ohlcv_to_df
from utils.strategies import BBStrategy

class Backtester():

  def __init__(self, initial_balance=1000, leverage=10, traling_stop_loss=False):
    self.initial_balance = initial_balance
    self.balance = initial_balance
    self.amount = 0
    self.leverage = leverage
    self.trailing_stop_loss = traling_stop_loss
    self.fee_cost = 0.02 / 100
    self.inv = self.balance * 0.01 * self.leverage
    self.profit = []
    self.drawdown = []
    self.winned_trades = 0
    self.lossed_trades = 0

    self.num_trades = 0
    self.num_long_trades = 0
    self.num_short_trades = 0

    self.is_long_position_open = False
    self.is_short_position_open = False

  def reset_report(self):
    self.balance = self.initial_balance
    self.amount = 0

    self.profit = []
    self.drawdown = []
    self.winned_trades = 0
    self.lossed_trades = 0

    self.num_trades = 0
    self.num_long_trades = 0
    self.num_short_trades = 0

    self.is_long_position_open = False
    self.is_short_position_open = False
  
  def open_position(self, price, side, from_opened):
    self.num_trades += 1

    if side == 'long':
      self.num_long_trades += 1
      
      if self.is_long_position_open:
        self.long_open_price = (self.long_open_price + self.long_open_price) / 2
        self.amount += self.inv / price
      else: 
        self.is_long_position_open = True
        self.long_open_price = price
        self.amount = self.inv / price

    elif side == 'short':
      self.num_short_trades += 1
      
      if self.is_short_position_open:
        self.short_open_price = (self.short_open_price + self.short_open_price) / 2
        self.amount += self.inv / price
      else:
        self.is_short_position_open = True
        self.short_open_price = price
        self.amount = self.inv / price

    else:
      raise ValueError('Side should be either long or short')
    
    if self.trailing_stop_loss:
      self.from_opened = from_opened
    
  def close_position(self, price):
    self.num_trades += 1

    if self.is_long_position_open:
      result = self.amount * (self.long_open_price - price)
      self.is_long_position_open = False
      self.long_open_price = 0

    elif self.is_short_position_open:
      result = self.amount * (price - self.short_open_price)
      self.is_short_position_open = False
      self.short_open_price = 0
      
    self.profit.append(result)
    self.balance += result

    if result > 0:
      self.winned_trades += 1
      self.drawdown.append(0)
    else:
      self.lossed_trades += 1
      self.drawdown.append(result)

    self.take_profit_price = 0
    self.stop_loss_price = 0

  def set_take_profit(self, price, tp_long=1.01, tp_short=0.99):
    if self.is_long_position_open:
      self.take_profit_price = price * tp_long

    elif self.is_short_position_open:
      self.stop_loss_price = price * tp_short

  def set_stop_loss(self, price, sl_long=0.99, sl_short=1.01):
    if self.is_long_position_open:
      self.stop_loss_price = price * sl_long

    elif self.is_short_position_open:
      self.stop_loss_price = price * sl_short

  def report(self, symbol, start_date, end_data):
    profit = np.sum(self.profit)
    drawdown = np.sum(self.drawdown)
    fees = np.abs(profit) * self.fee_cost * self.num_trades

    results = {
      'symbol': symbol,
      'start_date': start_date,
      'end_date': end_data,
      'initial_balance': self.initial_balance,
      'balance': self.balance,
      'profit': profit,
      'drawdown': drawdown,
      'fees': fees,
      'num_trades': self.num_trades,
      'num_long_trades': self.num_long_trades,
      'num_short_trades': self.num_short_trades,
      'winned_trades': self.winned_trades,
      'lossed_trades': self.lossed_trades,
    }

    return results

  def __backtesting__(self, df, strategy):
    hight = df['high']
    close = df['close']
    low = df['low']

    for i in range(len(df)):
      if self.balance > 0:
        if strategy.checkLongSignal(i):
          self.open_position(price=close[i], side='long', from_opened=i)
          self.set_take_profit(price=close[i], tp_long=1.03)
          self.set_stop_loss(price=close[i], sl_long=0.99)
        elif strategy.checkShortSignal(i):
          self.open_position(price=close[i], side='short', from_opened=i)
          self.set_take_profit(price=close[i], tp_short=0.97)
          self.set_stop_loss(price=close[i], sl_short=1.01)
        else:
          if self.trailing_stop_loss and (self.is_long_position_open or self.is_short_position_open):
            new_max_price = np.max(hight[self.from_opened:i])
            previous_stop_loss_price = self.stop_loss_price

            self.set_stop_loss(price=new_max_price)

            if previous_stop_loss_price > self.stop_loss_price:
              self.stop_loss_price = previous_stop_loss_price

          if self.is_long_position_open:
            if hight[i] >= self.take_profit_price:
              self.close_position(price=self.take_profit_price)
            elif low[i] <= self.stop_loss_price:
              self.close_position(price=self.stop_loss_price)
          
          if self.is_short_position_open:
            if hight[i] >= self.stop_loss_price:
              self.close_position(price=self.stop_loss_price)
            elif low[i] <= self.take_profit_price:
              self.close_position(price=self.take_profit_price)


if __name__ == '__main__':
  print('Backtester is starting...')

  exchange_id = 'binance'
  exchange_class = getattr(ccxt, exchange_id)
  exchange = exchange_class()

  ohclv = exchange.fetch_ohlcv('BTC/USDT', '1d', limit=1000)
  df = ccxt_ohlcv_to_df(ohclv)

  strategy = BBStrategy()
  strategy.setUp(df)

  tryback = Backtester()
  tryback.__backtesting__(df, strategy)
  report = tryback.report('BTC/USDT', '2021-01-01', '2021-12-31')
  print(report)
