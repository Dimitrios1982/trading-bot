import pandas as pd
import xgboost as xgb
import joblib
import numpy as np

# Load the model
model_filename = './models/xgboost_model.joblib'
bst = joblib.load(model_filename)

# Read the data from the file
data = pd.read_csv('./data/combined_data.csv')

# Drop the 'close' column
data = data.drop('close', axis=1)

# Extract features for the 3rd row
test_row = data.iloc[48].values.reshape(1, -1)
print(data.iloc[48])

# Convert to NumPy array
input_array = np.array(test_row)

# Make predictions directly using NumPy array
y_pred = bst.predict(input_array)

# Display the predicted value
print(f'Predicted Close Price: ${y_pred[0]:.2f}')
