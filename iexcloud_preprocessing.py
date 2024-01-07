import pandas as pd
import json

file_path = 'Data/'
file_name_prices = 'TSLA_core_historical_prices.csv'
prices_df = pd.read_csv(f'{file_path}{file_name_prices}')

file_name_sec = 'TSLA_core_reported_financials.csv'
sec_filings_df = pd.read_csv(f'{file_path}{file_name_sec}')

print(prices_df.head(5))
print(sec_filings_df)

sec_filings_columns = [
    "Revenues", "NetIncomeLoss", "EarningsPerShareBasic", "EarningsPerShareDiluted", 
    "OperatingIncomeLoss", "CostOfRevenue", "GrossProfit", 
    "CashAndCashEquivalentsAtCarryingValue", "LongTermDebt", "DebtCurrent", 
    "Assets", "LiabilitiesCurrent", "InventoryNet", "ResearchAndDevelopmentExpense"
]

sec_filings_df = sec_filings_df[sec_filings_columns]
sec_filings_df.to_csv(f'{file_path}{file_name_sec}_processed.csv', index=False)
print(sec_filings_df)



