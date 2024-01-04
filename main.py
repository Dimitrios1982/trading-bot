from api_handler import ApiHandler
import json

time_from = None  # Example: December 1, 2021
time_to = None    # Example: December 31, 2021

def beautify_json(data):
    return json.dumps(data, indent=2)

if __name__ == "__main__":
    api_handler = ApiHandler()

    # Example: Get stock data for a dynamically entered ticker symbol
    ticker_symbol = input("Enter the desired ticker symbol (e.g., IBM): ")
    stock_data = api_handler.get_daily_stock_data(ticker_symbol)
    print(f"\nDaily Stock Data for {ticker_symbol}:")
    print(beautify_json(stock_data))

    # Example: Get news sentiment for the same dynamically entered ticker symbol
    news_sentiment = api_handler.get_news_sentiment(ticker_symbol)
    if time_from is not None:
        news_sentiment = api_handler.get_news_sentiment(ticker_symbol, time_from=time_from, time_to=time_to)
        print(f"\nNews Sentiment for {ticker_symbol} between {time_from} and {time_to}:")
    else:
        print(f"\nNews Sentiment for {ticker_symbol}:")
    print(beautify_json(news_sentiment))

    # Example: Get advanced analytics for a dynamically entered ticker symbol
    ticker_symbol = input("Enter the desired ticker symbol (e.g., IBM): ")
    advanced_analytics_data = api_handler.get_advanced_analytics(ticker_symbol)
    print(f"\nAdvanced Analytics Data for {ticker_symbol}:")
