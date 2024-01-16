import pandas as pd

file_path = 'Data/TSLA_stock_indicator_ema.csv'
df = pd.read_csv(file_path)
print(df.iloc[:,0].head(5))
