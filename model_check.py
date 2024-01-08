import pandas as pd
import joblib

# Input data for prediction
input_data = {
      "priceDate": 1704412800000000000,
      "open": 236.86,
      "low": 235.5001,
      "high": 244.1196,
      "volume": 93488939.0,
      "Revenues": 23350000000,
      "NetIncomeLoss": 1853000000,
      "EarningsPerShareBasic": 0.58,
      "EarningsPerShareDiluted": 0.53,
      "OperatingIncomeLoss": 1764000000,
      "CostOfRevenue": 19172000000,
      "GrossProfit": 4178000000,
      "CashAndCashEquivalentsAtCarryingValue": 15932000000,
      "LongTermDebt": 2152000000,
      "DebtCurrent": 1552000000,
      "Assets": 93941000000,
      "LiabilitiesCurrent": 26640000000,
      "InventoryNet": 13721000000,
      "ResearchAndDevelopmentExpense": 1161000000
}

# Create a DataFrame from the input data
input_df = pd.DataFrame([input_data])

# Reshape input data to match the model's expected input shape
input_array = input_df.values.reshape((input_df.shape[0], 1, input_df.shape[1]))

# Load the trained model
model_filename = './models/TSLA_iexcloud_basic_rnn.joblib'
model = joblib.load(model_filename)

# Make predictions for the input data
predicted_close_price = model.predict(input_array)

# Display the predicted close price
print(f'Predicted Close Price: ${predicted_close_price[0][0]:.2f}')
