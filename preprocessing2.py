import pandas as pd

def extract_stock_data(json_data):
    time_series = json_data.get("Time Series (Daily)", {})
    stock_data_list = []
    
    for date, values in time_series.items():
        stock_data = {
            "date": date,
            "open": values.get("1. open"),
            "high": values.get("2. high"),
            "low": values.get("3. low"),
            "close": values.get("4. close"),
            "volume": values.get("5. volume")
        }
        stock_data_list.append(stock_data)

    return stock_data_list

# Example usage:
ticker = 'O'
daily_prices_file = f'./data/{ticker}_daily_stock_data.json'
daily_prices_data = pd.read_json(daily_prices_file)
stock_data = extract_stock_data(daily_prices_data)

# Convert to DataFrame for further analysis
stock_df = pd.DataFrame(stock_data)
print(stock_df.head())
