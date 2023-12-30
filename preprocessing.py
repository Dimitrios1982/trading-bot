import pandas as pd

ticker = 'O'

# Load and preprocess daily prices dataset
daily_prices_file = f'./data/{ticker}_daily_stock_data.json'
daily_prices_data = pd.read_json(daily_prices_file)
daily_prices_data = daily_prices_data['Time Series (Daily)'].apply(pd.Series).transpose()

# Load news sentiment dataset
news_sentiment_file = f'./data/{ticker}_news_sentiment.json'
news_sentiment_data = pd.read_json(news_sentiment_file)

# Check if the 'feed' key exists
if 'feed' in news_sentiment_data:
    # Extract relevant columns from the 'feed' key
    feed_data = news_sentiment_data['feed']
    if not feed_data.empty:
        # Use pd.json_normalize to flatten the nested structure
        sentiment_entries = pd.json_normalize(feed_data)[['time_published', 'overall_sentiment_score']]
        # Convert the time_published column to datetime with the same format as daily_prices
        sentiment_entries['time_published'] = pd.to_datetime(sentiment_entries['time_published']).dt.strftime('%Y-%m-%d')

        # Merge datasets based on the date, filling missing sentiment scores with 0
        combined_data = pd.merge(daily_prices_data, sentiment_entries, left_index=True, right_on='time_published', how='left')
        combined_data['overall_sentiment_score'] = combined_data['overall_sentiment_score'].fillna(0)

        # Reorganize data to have sentiment scores on the same row as the corresponding date
        print(combined_data.columns)
        #combined_data = combined_data[['1. open', '2. high', '3. low', '4. close', '5. volume', 'overall_sentiment_score']]
        combined_data = combined_data[['time_published', 'overall_sentiment_score'] + daily_prices_data.columns.tolist()]
        combined_data.to_json("./data/combined_data.json", orient='records', indent=2)


        # Display the resulting combined dataset
        print(combined_data.head())
    else:
        print("'feed' key is empty.")
else:
    print("'feed' key not found in news_sentiment_data.")
