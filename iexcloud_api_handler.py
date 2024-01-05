import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
import os
import json



def _encode_params(params):
    return urlencode(params)

def get_data(workspace, dataset_id,symbol, params):
    base_url = f"https://api.iex.cloud/v1/data/{workspace}/{dataset_id}/{symbol}?{params}"
    print(base_url)
    response = requests.get(base_url)
    data = response.json()
    
    file_path = os.path.join('Data', f'{symbol}_{workspace}_{dataset_id}.json')
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"{workspace} {dataset_id} for {symbol} saved to {file_path}")

