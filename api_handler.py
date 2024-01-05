import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
import os
import json

class ApiHandler:
    def __init__(self, api_key=None):
        if api_key is None:
            load_dotenv()
            api_key = os.environ.get('ALPHA_VANTAGE_API_KEY2')

        self.api_key = api_key
        self.base_url = 'https://alphavantageapi.co/'

    def _make_request(self, function, params):
        params['apikey'] = self.api_key
        url = f"{self.base_url}query{function}&{self._encode_params(params)}"
        print(url)
        response = requests.get(url)
        return response

    def _encode_params(self, params):
        return urlencode(params)

    def _save_to_file(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def get_daily_stock_data(self, symbol):
        function = '?function=TIME_SERIES_DAILY'
        params = {'symbol': symbol}
        response = self._make_request(function, params)
        data = response.json()
        self._save_to_file(data, f'./data/{symbol}_daily_stock_data.json')
        return data

    def get_news_sentiment(self, tickers, time_from=None, time_to=None, limit=None):
        function = '?function=NEWS_SENTIMENT'
        params = {'tickers': tickers, 'limit': limit}

        # Include time_from and time_to only if provided
        if time_from:
            params['time_from'] = time_from
        if time_to:
            params['time_to'] = time_to

        response = self._make_request(function, params)
        data = response.json()
        self._save_to_file(data, f'./data/{tickers}_news_sentiment.json')
        return data

    def get_advanced_analytics(self, symbol, date_range='full', ohlc='close', interval='DAILY',
                               calculations='MIN,MAX,MEAN,MEDIAN,CUMULATIVE_RETURN,VARIANCE,STDDEV,HISTOGRAM,AUTOCORRELATION,COVARIANCE,CORRELATION'):
        function = 'timeseries/analytics'
        # Define parameters
        params = {
            'SYMBOLS': symbol,
            'RANGE': date_range,
            'OHLC': ohlc,
            'INTERVAL': interval,
            'CALCULATIONS': calculations,
            'apikey': self.api_key
        }

        # Make the API request
        response = self._make_request(function, params)
        data = response.json()

        # Define the file path
        file_path = os.path.join('Data', f'{symbol}_advanced_analytics.json')

        # Save the data to the specified file
        with open(file_path, 'w') as file:
            json.dump(data, file)

        print(f"Advanced analytics data for {symbol} saved to {file_path}")

        return data
