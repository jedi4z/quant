import pandas as pd

if __name__ == "__main__":
  pd.options.display.max_rows = 4
  pd.options.display.precision = 2
  data = pd.read_excel('AAPL.xlsx', sheet_name='Hoja1')
  data['intraday_variation'] = 100 * (data['close'] - data['open']) / data['open']
  data.to_excel('AAPL_ej3.xlsx', sheet_name='ej3', columns=['timestamp', 'intraday_variation'])

  print(data)

