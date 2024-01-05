import iexcloud_api_handler as iex
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get('IEXCLOUD_API_KEY')

params = {'token': api_key,
          'range': "5y",
          'sort': "DESC"
         }
params = iex._encode_params(params)

# Get core historical equity prices
iex.get_data(workspace="core", dataset_id="historical_prices", symbol="TSLA", params=params)