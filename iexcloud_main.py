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
params_sec_filings = { 
    'token': api_key,
    'format': 'csv'

    }

iex.get_data(workspace="core", dataset_id="reported_financials", symbol= tickers, params=params_sec_filings, sec_filing_type="10-Q")

## Get sector performance ##
params_sector_performance = {
    'token': api_key,
    'from': '2023-01-01',
    'to': '2024-01-15',
    'on': '2024-01-10',
    'sort': 'desc',
    'format': 'csv'
}
iex.get_data(workspace="core", dataset_id="sector_performance", symbol='market', params=params_sector_performance)

## Get indicator ##
params_indicators = {
    'token': api_key,
    'range': "5y",
    'sort': "desc",
    'format': 'csv',
    'indicatorOnly': True,
    'period': 26
}
iex.get_data(workspace="stock", dataset_id='indicator', symbol= tickers, params=params_indicators, indicator='ema')
