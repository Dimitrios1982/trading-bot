import pandas as pd
import joblib

# Input data for prediction
input_data = {
    'open': 58.0,
    'high': 58.12,
    'low': 57.4,
    'volume': 6690000,
    'overall_sentiment_score': 0.5  # Provide a sentiment score based on your criteria
}

# Create a DataFrame from the input data
input_df = pd.DataFrame([input_data])

# Load the trained model
model_filename = './models/stock_price_prediction_model.joblib'
model = joblib.load(model_filename)

# Make predictions for the input data
predicted_close_price = model.predict(input_df[['open', 'high', 'low', 'volume', 'overall_sentiment_score']])

# Display the predicted close price
print(f'Predicted Close Price: ${predicted_close_price[0]:.2f}')
