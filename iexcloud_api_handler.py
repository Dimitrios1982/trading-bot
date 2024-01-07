import requests
from dotenv import load_dotenv
from urllib.parse import urlencode
import os
import json



def _encode_params(params):
    return urlencode(params)

def get_data(workspace, dataset_id,symbol, params, sec_filing_type= None):
    params = _encode_params(params)
    if sec_filing_type == None:
        base_url = f"https://api.iex.cloud/v1/data/{workspace}/{dataset_id}/{symbol}?{params}"
        file_path = os.path.join('Data', f'{symbol}_{workspace}_{dataset_id}.csv')
    elif sec_filing_type != None:
        base_url = f"https://api.iex.cloud/v1/data/{workspace}/{dataset_id}/{symbol}/{sec_filing_type}?{params}"
        file_path = os.path.join('Data', f'{symbol}_{workspace}_{dataset_id}_{sec_filing_type}.csv')
    print(base_url)
    response = requests.get(base_url)
    
    file_path = os.path.join('Data', f'{symbol}_{workspace}_{dataset_id}.csv')
    with open(file_path, 'w', newline='') as file:
        file.write(response.text)
    print(f"{workspace} {dataset_id} for {symbol} saved to {file_path}")

