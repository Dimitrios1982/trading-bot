import pandas as pd
import numpy as np

file_path = 'Data/'

# Preprocess stock prices
file_name_prices = 'TSLA_core_historical_prices.csv'
prices_df = pd.read_csv(f'{file_path}{file_name_prices}')

prices_columns = ["priceDate", "open", "low", "high", "close", "volume"]

prices_df = prices_df[prices_columns]
date_column = prices_df["priceDate"] 
prices_df["priceDate"] = pd.to_datetime(date_column).astype(np.int64)    # Convert the date column to a numeric representation (e.g., timestamp)
prices_df.to_csv(f'{file_path}{file_name_prices}_preprocessed.csv', index=False)

# Preprocess SEC filings
file_name_sec = 'TSLA_core_reported_financials.csv'
sec_filings_df = pd.read_csv(f'{file_path}{file_name_sec}')

sec_filings_columns = [
    "Revenues", "NetIncomeLoss", "EarningsPerShareBasic", "EarningsPerShareDiluted", 
    "OperatingIncomeLoss", "CostOfRevenue", "GrossProfit", 
    "CashAndCashEquivalentsAtCarryingValue", "LongTermDebt", "DebtCurrent", 
    "Assets", "LiabilitiesCurrent", "InventoryNet", "ResearchAndDevelopmentExpense"
]

sec_filings_df = sec_filings_df[sec_filings_columns]
sec_filings_df.to_csv(f'{file_path}{file_name_sec}_processed.csv', index=False)
print(sec_filings_df)

# Repeat the first row of sec_filings_df to fill missing entries
sec_filings_repeated = pd.concat([sec_filings_df] * len(prices_df), ignore_index=True)

# Merge the two DataFrames
merged_df = pd.concat([prices_df, sec_filings_repeated], axis=1)
merged_df.to_csv(f'{file_path}combined_data.csv', index=False)
print(merged_df.head(5))

