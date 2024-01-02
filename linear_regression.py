import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import os

# Get the script filename
script_path = os.path.abspath(__file__)
script_filename = os.path.basename(script_path)
script_filename = os.path.splitext(script_filename)[0]

ticker = 'O'

# Load the combined dataset
combined_data_file = './data/O_combined_data.csv'
combined_data = pd.read_csv(combined_data_file)

# Drop rows with missing values
combined_data = combined_data.dropna()

# Features (X) and target variable (y)
features = combined_data.drop(['date', 'close'], axis=1)
target = combined_data['close']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize the model (replace with your chosen model)
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Save the trained model
model_filename = f'./models/{ticker}_{script_filename}.joblib'
joblib.dump(model, model_filename)

print(f'Model saved to {model_filename}')
