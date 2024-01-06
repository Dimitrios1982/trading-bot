import pandas as pd
import json

prices_df = pd.read_csv('Data/TSLA_core_historical_prices.csv')
print(prices_df.head(5))

sec_filings_columns = [
    "Revenue",
    "NetIncomeLoss",
    "EarningsPerShareBasic",
    "EarningsPerShareDiluted",
    "OperatingIncomeLoss",
    "CostOfRevenue",
    "GrossProfit",
    "CashAndCashEquivalentsAtCarryingValue",
    "LongTermDebt",
    "DebtCurrent",
    "Assets",
    "LiabilitiesCurrent",
    "LiabilitiesNoncurrent",
    "FreeCashFlow",
    "ROE",
    "Dividends",
    "InventoryNet",
    "ResearchAndDevelopmentExpense",
    "MarketCapitalization",
    "StockRepurchasedAndRetiredDuringPeriodValue",
    "ShareBasedCompensation"
]