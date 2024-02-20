import pandas as pd
from datetime import datetime

file_path = 'data/'

# Preprocess stock prices
file_name_prices = 'TSLA_core_historical_prices.csv'
prices_df = pd.read_csv(f'{file_path}{file_name_prices}')

prices_columns = ["priceDate", "open", "low", "high", "close", "volume"]

prices_df = prices_df[prices_columns]

# Convert the 'priceDate' column to datetime
prices_df["priceDate"] = pd.to_datetime(prices_df["priceDate"])

# Convert 'priceDate' column to Unix time
prices_df["priceDate"] = prices_df["priceDate"].apply(lambda x: datetime.timestamp(x))

# Drop rows with missing values in the 'priceDate' column
prices_df = prices_df.dropna(subset=['priceDate'])

# Save preprocessed data
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

# Repeat the first row of sec_filings_df to fill missing entries
sec_filings_repeated = pd.concat([sec_filings_df] * len(prices_df), ignore_index=True)

# Load weather data
weather_data_file = f'{file_path}weather_data.csv'
weather_data = pd.read_csv(weather_data_file)

# Convert 'date' column to datetime
weather_data['date'] = pd.to_datetime(weather_data['date']).dt.date

# Convert 'date' column to Unix time
weather_data['date'] = weather_data['date'].apply(lambda x: datetime.timestamp(datetime.combine(x, datetime.min.time())))

# Merge the DataFrames based on 'priceDate' from prices_df and 'date' from weather_data
merged_df = pd.merge(prices_df, sec_filings_repeated, left_index=True, right_index=True)

# Merge weather_data with merged_df
merged_df = pd.merge(merged_df, weather_data, left_on='priceDate', right_on='date', how='inner')

# Drop the redundant 'date' column
merged_df.drop(columns=['date'], inplace=True)

# Save the merged data to a CSV file
merged_df.to_csv(f'{file_path}combined_data.csv', index=False)

print("Merged DataFrame:")
print(merged_df.head(5))
