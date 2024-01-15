import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost_model import XGBRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Load combined_data
combined_data = pd.read_csv('./data/combined_data.csv')  # Replace with the actual path

# Drop rows with missing values
combined_data = combined_data.dropna()

# Extract features (X) and target variable (y)
features = combined_data.drop(columns=["close"])
target = combined_data["close"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize the XGBoost model
model = XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 100)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error on Test Set: {mse:.4f}')

# Save the trained model
joblib.dump(model, './models/xgboost_model.joblib')
print('XGBoost Model saved to ./models/xgboost_model.joblib')
