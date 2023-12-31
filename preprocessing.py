import pandas as pd
import json

ticker = 'O'

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

def extract_sentiment_data(json_data):
    feed = json_data.get("feed", [])

    # Extract sentiment data into a list of dictionaries
    sentiment_data_list = []
    for entry in feed:
        sentiment_data = {
            "date": pd.to_datetime(entry["time_published"], format='%Y%m%dT%H%M%S', errors='coerce'),
            "time_published": pd.to_datetime(entry["time_published"], format='%Y%m%dT%H%M%S', errors='coerce'),
            "overall_sentiment_score": entry["overall_sentiment_score"]
        }
        sentiment_data_list.append(sentiment_data)

    # Create a DataFrame from the list of dictionaries
    sentiment_df = pd.DataFrame(sentiment_data_list)

    return sentiment_df.rename(columns={"time_published": "time_published_sentiment"})  # Rename the column


def preprocess_sentiment_data(sentiment_df):
    # Drop the 'date' column
    sentiment_df = sentiment_df.drop(columns=['date'])

    # Format 'time_published' to display only yyyy-mm-dd
    sentiment_df['time_published_sentiment'] = sentiment_df['time_published_sentiment'].dt.strftime('%Y-%m-%d')

    # Convert 'overall_sentiment_score' to numeric
    sentiment_df['overall_sentiment_score'] = pd.to_numeric(sentiment_df['overall_sentiment_score'], errors='coerce')

    # Group by 'time_published' and calculate the mean of 'overall_sentiment_score'
    sentiment_df = sentiment_df.groupby('time_published_sentiment').mean().reset_index()

    return sentiment_df


daily_prices_file = f'./data/{ticker}_daily_stock_data.json'
news_sentiment_file = f'./data/{ticker}_news_sentiment.json'
combined_data_file = f'./data/{ticker}_combined_data.csv'
daily_stock_data = f'./data/{ticker}_daily_stock_data.csv'

# Read daily stock data
with open(daily_prices_file) as file:
    daily_prices_data = json.load(file)

# Extract stock data
stock_data = extract_stock_data(daily_prices_data)

# Convert stock data to DataFrame
stock_df = pd.DataFrame(stock_data)

# Save the stock data to a CSV file
stock_df.to_csv(daily_stock_data, index=False)

# Read news sentiment data
with open(news_sentiment_file) as file:
    news_sentiment_data = json.load(file)

# Extract sentiment data
sentiment_data = extract_sentiment_data(news_sentiment_data)

# Preprocess sentiment data
sentiment_data = preprocess_sentiment_data(sentiment_data)

# Merge the two datasets on 'time_published'
combined_data = pd.merge(stock_df, sentiment_data, left_on='date', right_on='time_published_sentiment', how='left')

# Fill NaN values with 0 in 'overall_sentiment_score' column
combined_data['overall_sentiment_score'] = combined_data['overall_sentiment_score'].fillna(0)

# Drop the 'time_published_sentiment' column
combined_data = combined_data.drop(columns=['time_published_sentiment'])

# Save the combined data to a CSV file
combined_data.to_csv(combined_data_file, index=False)

print(f"Combined data saved to {combined_data_file}")
print(combined_data.head())
