import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense


ticker = 'TSLA'

# Get the script filename
script_path = os.path.abspath(__file__)
script_filename = os.path.basename(script_path)
script_filename = os.path.splitext(script_filename)[0]

# Load combined_data
combined_data = pd.read_csv(f'./data/combined_data.csv')  # Replace with the actual path

# Drop rows with missing values
combined_data = combined_data.dropna()

# Extract features (X) and target variable (y)
features = combined_data.drop(columns=["close"])
target = combined_data["close"]

print("columns: ", features.columns)

# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
target_scaled = scaler.fit_transform(target.values.reshape(-1, 1))


# Split the data into training and testing sets
#X_train, X_test, y_train, y_test = train_test_split(features_scaled, target_scaled, test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Reshape features for RNN input (samples, time steps, features)
X_train_reshaped = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test_reshaped = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# Build a simple RNN model
model = Sequential()
model.add(SimpleRNN(units=50, activation='relu', input_shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2])))
model.add(Dense(units=25, activation='relu')),
model.add(Dense(units=25, activation='relu')),
model.add(Dense(units=1, activation='linear'))  # Output layer with linear activation for regression

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train_reshaped, y_train, epochs=1000, batch_size=32, validation_split=0.15, verbose=1)

# Evaluate the model on the test set
loss = model.evaluate(X_test_reshaped, y_test)
print(f'Mean Squared Error on Test Set: {loss}')

# Save the trained model
model_filename = f'./models/{ticker}_{script_filename}.joblib'
joblib.dump(model, model_filename)

print(f'Model saved to {model_filename}')

# Make predictions
predictions = model.predict(X_test_reshaped)

# You can use 'predictions' to analyze the model's performance or make further predictions.
