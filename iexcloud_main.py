import iexcloud_api_handler as iex
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get('IEXCLOUD_API_KEY')

# Example for multiple tickers ["TSLA", "IBM", "AAPL"]
tickers = ["TSLA"] 
tickers = ','.join(tickers)

# Parameters for core historical equity prices
params_prices = {
    'token': api_key,
    'range': "5y",
    'sort': "DESC",
    'format': 'csv'
    }

## Get core historical equity prices ##
iex.get_data(workspace="core", dataset_id="historical_prices", symbol= tickers, params=params_prices)

## Get SEC filings ##
params_sec = { 
    'token': api_key,
    'format': 'csv'

    }

iex.get_data(workspace="core", dataset_id="reported_financials", symbol= tickers, params=params_sec, sec_filing_type="10-Q")

