import pandas as pd

if  __name__ == '__main__':
  data = pd.read_excel('AAPL.xlsx', sheet_name='Hoja1')

  filtered_data = data.set_index('timestamp')
  filtered_data = filtered_data.loc['2008-05-15']

  print("data of 2008-05-15")
  print(filtered_data)